from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse
from egy_lens.funcatoins import predict_and_detect
from ultralytics import YOLO
import os
import cv2
import numpy as np  # Import NumPy

base_dir = os.path.dirname(os.path.abspath(__file__))
model = YOLO(os.path.join(base_dir, "best.pt"))


# Create your views here.
@api_view(["POST"])
def process_image(request):
    if request.method == "POST":
        # Assuming the image is sent as a form field named 'image'
        uploaded_image = request.FILES.get("image")
        if uploaded_image:
          
            image_data = (
                uploaded_image.read()
            )  # Read the image data from the file object
            np_array = np.frombuffer(
                image_data, np.uint8
            )  # Convert the image data to a NumPy array
            image = cv2.imdecode(
                np_array, cv2.IMREAD_COLOR
            )  # Decode the image array into an OpenCV image object

            result_img, predicted_labels = predict_and_detect(
                model, image, classes=[], conf=0.5
            )
            print("hi", predicted_labels)
            data = [
                {
                    "Predicted_Labels": "thing",
                }
            ]
            processed_data = {"result":predicted_labels[0] }
            return JsonResponse(processed_data)
        else:
            return JsonResponse({"error": "No image uploaded"}, status=400)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
