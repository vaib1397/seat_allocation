from pickle import TRUE
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins, generics
from rest_framework.permissions import IsAuthenticated
from profiles.models import Room, School, Seat, SeatHistory, Student, User
from profiles.serializer import (
    ChangeRoomSerializer,
    SchoolSerializer,
    SeatHistorySerializer,
    SeatSerializer,
    StudentSerializer,
    UserSerializer,
    RoomSerializer,
)


class GetStudentsView(APIView):
    def get(self, request):
        params = request.query_params
        room_id = params.get("room_id")
        if not room_id:
            return Response({"error": "No room id provided"}, status=400)
        room = get_object_or_404(Room, pk=room_id)
        students = room.get_students()
        return Response(StudentSerializer(students, many=True).data, status=200)


class RoomView(APIView):
    def get(self, request):
        params = request.query_params
        count = params.get("number_of_employees", 15)
        rooms = Room.objects.filter(current_student_count__gte=count)
        return Response(RoomSerializer(rooms, many=True).data, status=200)


class ChangeRoomView(APIView):
    def post(self, request):
        data = request.data
        ser = ChangeRoomSerializer(data=data)
        ser.is_valid(raise_exception=True)
        new_seat_history = ser.save()
        return Response("Changed room successfully", status=201)


class UserlistView(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = UserSerializer
    permission_class = [IsAuthenticated]
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        params = request.query_params
        if not "pk" in kwargs:
            return self.list(request)
        post = get_object_or_404(User, pk=kwargs["pk"])
        return Response(UserSerializer(post).data, status=200)

    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            post = serializer.save()
            return Response(UserSerializer(post).data, status=201)
        return Response(serializer.errors, status=400)


class StudentlistView(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.DestroyModelMixin
):
    serializer_class = StudentSerializer
    permission_class = [IsAuthenticated]
    queryset = Student.objects.all()

    def get(self, request, *args, **kwargs):
        if not "pk" in kwargs:
            return self.list(request)
        post = get_object_or_404(Student, pk=kwargs["pk"])
        return Response(StudentSerializer(post).data, status=200)

    def post(self, request):
        data = request.data
        serializer = StudentSerializer(data=data)
        if serializer.is_valid():
            post = serializer.save()
            return Response(StudentSerializer(post).data, status=201)
        return Response(serializer.errors, status=400)

    def patch(self, request, pk=None):
        instance = self.get_object(pk)
        ser = StudentSerializer(instance, data=request.data, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=200)
        return Response(ser.errors, status=400)

    def delete(self, request):
        return self.destroy(request, id)


class SchoollistView(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = SchoolSerializer
    permission_class = [IsAuthenticated]
    queryset = School.objects.all()

    def get(self, request, *args, **kwargs):
        if not "pk" in kwargs:
            return self.list(request)
        post = get_object_or_404(School, pk=kwargs["pk"])
        return Response(SchoolSerializer(post).data, status=200)

    def post(self, request):
        data = request.data
        serializer = SchoolSerializer(data=data)
        if serializer.is_valid():
            post = serializer.save()
            return Response(SchoolSerializer(post).data, status=201)
        return Response(serializer.errors, status=400)

    def patch(self, request, pk=None):
        instance = self.get_object(pk)
        ser = SchoolSerializer(instance, data=request.data, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=200)
        return Response(ser.errors, status=400)


class RoomlistView(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = RoomSerializer
    permission_class = [IsAuthenticated]
    queryset = Room.objects.all()

    def get(self, request, *args, **kwargs):
        if not "pk" in kwargs:
            return self.list(request)
        post = get_object_or_404(Room, pk=kwargs["pk"])
        return Response(RoomSerializer(post).data, status=200)

    def post(self, request):
        data = request.data
        serializer = RoomSerializer(data=data)
        if serializer.is_valid():
            post = serializer.save()
            return Response(RoomSerializer(post).data, status=201)
        return Response(serializer.errors, status=400)


class SeatHistoryListView(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = SeatHistorySerializer
    permission_class = [IsAuthenticated]
    queryset = SeatHistory.objects.all().order_by("-filled_at")

    def get(self, request, *args, **kwargs):
        return self.list(request)


class SeatlistView(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = SeatSerializer
    permission_class = [IsAuthenticated]
    queryset = Seat.objects.all()

    def get(self, request, *args, **kwargs):
        if not "pk" in kwargs:
            return self.list(request)
        post = get_object_or_404(Seat, pk=kwargs["pk"])
        return Response(SeatSerializer(post).data, status=200)

    def post(self, request):
        data = request.data
        serializer = SeatSerializer(data=data)
        if serializer.is_valid():
            post = serializer.save()
            return Response(SeatSerializer(post).data, status=201)
        return Response(serializer.errors, status=400)
