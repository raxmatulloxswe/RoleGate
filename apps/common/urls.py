from django.urls import path

from .views import hello

app_name = "common"

urlpatterns = [
    path("", hello.as_view(), name="hello"),
]