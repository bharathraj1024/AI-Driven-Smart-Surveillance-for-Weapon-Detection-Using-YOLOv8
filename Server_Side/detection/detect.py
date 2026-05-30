import os
import sys
import cv2
from datetime import datetime
from django.core.files.base import ContentFile
import django

# Step 1: Add the base project path to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)  # Ensure it's at the front

# Step 2: Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wd_ss.settings')

# Step 3: Setup Django
django.setup()

# Now safe to import Django stuff
from wd_ss.storage_backends import PublicMediaStorage


def save_frame_to_s3(frame):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"media/weapon_{timestamp}.jpg"  # Save to media folder in S3

    # Convert frame to JPEG
    success, buffer = cv2.imencode(".jpg", frame)
    if not success:
        print("❌ Failed to encode frame.")
        return

    content = ContentFile(buffer.tobytes())

    # Use your custom S3 storage class
    s3_storage = PublicMediaStorage()
    saved_path = s3_storage.save(filename, content)

    print(f"✅ Image uploaded to S3: {saved_path}")


def detect_and_upload():
    cap = cv2.VideoCapture(0)  # Open webcam

    if not cap.isOpened():
        print("❌ Could not open webcam.")
        return

    print("🎥 Webcam started. Press 's' to save frame, 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to grab frame.")
            break

        cv2.imshow("Live Detection", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):
            save_frame_to_s3(frame)
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    detect_and_upload()
