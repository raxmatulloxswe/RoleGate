from django.urls import path

from .views import hello, StatisticsForManagerApiView, StatisticsForAdminApiView

app_name = "common"

urlpatterns = [
    path("", hello.as_view(), name="hello"),
    path('statistics/', StatisticsForManagerApiView.as_view(), name='statics'),
    path('statistics/admin/', StatisticsForAdminApiView.as_view(), name='statics_admin'),
]