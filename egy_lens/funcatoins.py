import cv2
from ultralytics import YOLO
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
model = YOLO(os.path.join(base_dir, "best.pt"))


def predict(chosen_model, img, classes=None, conf=0.5):
    if classes is None:
        classes = []
    if classes:
        results = chosen_model.predict(img, classes=classes, conf=conf)
    else:
        results = chosen_model.predict(img, conf=conf)

    return results


def predict_and_detect(chosen_model, img, classes=None, conf=0.5):
    if classes is None:
        classes = []
    results = predict(chosen_model, img, classes, conf=conf)
    predicted_labels = []

    for result in results:
        for box in result.boxes:
            predicted_labels.append(result.names[int(box.cls[0])])
            cv2.rectangle(
                img,
                (int(box.xyxy[0][0]), int(box.xyxy[0][1])),
                (int(box.xyxy[0][2]), int(box.xyxy[0][3])),
                (255, 0, 0),
                2,
            )
            cv2.putText(
                img,
                f"{result.names[int(box.cls[0])]}",
                (int(box.xyxy[0][0]), int(box.xyxy[0][1]) - 10),
                cv2.FONT_HERSHEY_PLAIN,
                1,
                (255, 0, 0),
                1,
            )
    return img, predicted_labels


# read the image
# imge = cv2.imread("photo_2024-05-03_20-37-26.jpg")

# result_img, predicted_labels = predict_and_detect(model, imge, classes=[], conf=0.5)
# print("Predicted Labels:", predicted_labels[0])


# # فتح الكاميرا
# cap = cv2.VideoCapture(0)
#
# # التحقق من ما إذا تم فتح الكاميرا بنجاح
# if not cap.isOpened():
#     print("Could not open camera")
#     exit()
#
# while True:
#     # قراءة الإطار من الكاميرا
#     ret, frame = cap.read()
#
#     if not ret:
#         print("Can't receive frame (stream end?). Exiting ...")
#         break
#
#     result_img, predicted_labels = predict_and_detect(model, frame, classes=[], conf=0.5)
#     print("Predicted Labels:", predicted_labels)
#
#     cv2.imshow("Image", result_img)
#     cv2.imwrite("YourSavePath", result_img)
#
#     # انتظار لضغط مفتاح "q" لإنهاء البرنامج
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# # تحرير الكاميرا وإغلاق النوافذ
# cap.release()
# cv2.destroyAllWindows()
