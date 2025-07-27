import cv2
import face_recognition
import pickle
import os
from PIL import Image
import numpy as np
import firebase_admin
from firebase_admin import credentials, db, storage

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendencerealtime-fa046-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendencerealtime-fa046.appspot.com"
})
bucket = storage.bucket()

folderPath = 'Images'
print("\n=== Cleaning & Preparing Images ===")

# Step 1: Force-clean images to standard 8‑bit RGB JPEG
for filename in os.listdir(folderPath):
    file_path = os.path.join(folderPath, filename)
    try:
        # Load with Pillow & convert to RGB
        pil_img = Image.open(file_path).convert('RGB')
        # Create new clean RGB image & paste
        clean_img = Image.new("RGB", pil_img.size, (255, 255, 255))
        clean_img.paste(pil_img)
        clean_name = os.path.splitext(filename)[0] + ".jpg"
        save_path = os.path.join(folderPath, clean_name)
        clean_img.save(save_path, "JPEG", quality=95)
        if clean_name != filename:
            os.remove(file_path)
        print(f"✅ Cleaned & saved: {clean_name}")
    except Exception as e:
        print(f"⚠️ Skipping {filename}: {e}")

print("\n=== Loading Images for Encoding ===")
pathList = os.listdir(folderPath)
print("Found images:", pathList)

imgList = []
studentIds = []
for path in pathList:
    filePath = os.path.join(folderPath, path)
    try:
        # Reopen with OpenCV (forces 8‑bit BGR), then convert to RGB
        img_cv = cv2.imread(filePath)
        if img_cv is None:
            print(f"⚠️ Skipping {path}: Could not read with OpenCV.")
            continue
        img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
        img_rgb = np.ascontiguousarray(img_rgb)  # Ensure contiguous memory
        imgList.append(img_rgb)
        studentIds.append(os.path.splitext(path)[0])

        # Upload to Firebase
        blob = bucket.blob(f'{folderPath}/{path}')
        blob.upload_from_filename(filePath)
    except Exception as e:
        print(f"⚠️ Skipping {path}: {e}")

print("Student IDs:", studentIds)

# Step 3: Encode faces
def findEncodings(imagesList):
    encodeList = []
    for idx, img in enumerate(imagesList):
        try:
            faces = face_recognition.face_encodings(img)
            if len(faces) > 0:
                encodeList.append(faces[0])
                print(f"✅ Face encoded for {studentIds[idx]}")
            else:
                print(f"⚠️ No face found in image {studentIds[idx]}, skipping.")
        except Exception as e:
            print(f"⚠️ Error processing {studentIds[idx]}: {e}")
    return encodeList

print("\nEncoding Started ...")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Encoding Complete")

with open("EncodeFile.p", 'wb') as file:
    pickle.dump(encodeListKnownWithIds, file)
print("File Saved: EncodeFile.p")
