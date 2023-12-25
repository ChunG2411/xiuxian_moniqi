from django.urls import path

from app_user.views import (
    RegisterUser,
    CharactersView
)

urlpatterns = [
    path('register/', RegisterUser.as_view(), name="register"),
    path('characters/', CharactersView.as_view(), name="characters"),

]
