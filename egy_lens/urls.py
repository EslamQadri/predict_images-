from django.urls import path
from egy_lens.views import process_image, index

urlpatterns = [
    path("api/process-image/", process_image, name="process_image"),
    path("", index, name="index"),
]
