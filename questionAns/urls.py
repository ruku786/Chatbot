from django.urls import path
from .views import *

urlpatterns = [
    path("getid/",User_id.as_view(),name="getid"),
    path("chat/",ChatAnswer.as_view(),name="chat"),
    path("index/", index, name="index")
]