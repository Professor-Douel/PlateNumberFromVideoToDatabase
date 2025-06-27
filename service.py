import os
import cv2
import easyocr
import re
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from db.engine import SessionLocal
from db.models import DBPlateNumber


if not os.path.exists('screenshots'):
    os.makedirs('screenshots')


pattern = re.compile(r'^[A-Z]{2}[0-9]{4}[A-Z]{2}$')


MIN_INTERVAL_SECONDS = 10
recent_plates: dict[str, datetime] = {}

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

number_cascade = cv2.CascadeClassifier('AIModels/plate_number.xml')
reader = easyocr.Reader(['en'], gpu=True)

db: Session = SessionLocal()

while True:
    success, img = cap.read()
    if not success:
        break

    results = number_cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=3)

    for (x, y, w, h) in results:
        roi = img[y:y + h, x:x + w]
        ocr_result = reader.readtext(roi)

        for detection in ocr_result:
            plate_text = detection[1].replace(" ", "").upper()

            if len(plate_text) == 8 and pattern.match(plate_text):
                now = datetime.utcnow()
                last_seen = recent_plates.get(plate_text)

                if not last_seen or (now - last_seen) > timedelta(seconds=MIN_INTERVAL_SECONDS):

                    new_plate = DBPlateNumber(
                        plate_number=plate_text,
                        date_created=now
                    )
                    db.add(new_plate)
                    db.commit()
                    print(f"Saved plate: {plate_text}")


                    filename = f"screenshots/{plate_text}_{now.strftime('%Y%m%d_%H%M%S')}.jpg"
                    cv2.imwrite(filename, img)
                    print(f"Screenshot saved as {filename}")


                    recent_plates[plate_text] = now
                else:
                    print(f"Skipped (too soon): {plate_text}")

            cv2.putText(img, plate_text, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('Result', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

db.close()
cap.release()
cv2.destroyAllWindows()
