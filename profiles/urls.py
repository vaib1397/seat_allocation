from django.urls import path

from profiles.views import *

urlpatterns = [
    path("student", StudentlistView.as_view()),
    path("student/<int:pk>", StudentlistView.as_view()),
    path("school", SchoollistView.as_view()),
    path("user", UserlistView.as_view()),
    path("user/<int:pk>", UserlistView.as_view()),
    path("room", RoomlistView.as_view()),
    path("room/<int:pk>", RoomlistView.as_view()),
    path("seat", SeatlistView.as_view()),
    # Questions
    path("get-students-via-room", GetStudentsView.as_view()),
    path("room_from_student_count", RoomView.as_view()),
    path("seat-details", SeatHistoryListView.as_view()),
    path("change-room", ChangeRoomView.as_view()),
]
