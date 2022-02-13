from django.db import models, transaction
from main.mixins import Timestampedmodel
from django.contrib.auth.models import User
from django.contrib import admin
from django.db.models import Count
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser, Timestampedmodel):
    username = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64, null=True, blank=True)


class School(Timestampedmodel):
    name = models.CharField(max_length=64, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=150)


class Student(Timestampedmodel):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def get_seat(self, date):
        seat_history = SeatHistory.objects.filter(
            student_id=self.id, filled_at__date__lte=date, vacant_at__date__gte=date
        ).last()
        return seat_history.seat


class Room(Timestampedmodel):
    name = models.CharField(max_length=64)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    capacity = models.IntegerField(default=0)
    current_student_count = models.IntegerField(default=0)

    def get_students(self):
        seat_history = SeatHistory.objects.filter(
            seat__room=self, vacant_at__isnull=True
        )
        student_ids = seat_history.values_list("student_id", flat=True)
        students = Student.objects.filter(id__in=student_ids)
        return students

    def add_seat(self):
        Seat.objects.create(room=self)
        return True

    @transaction.atomic
    def add_student(self, student_id):
        seat = Seat.objects.filter(is_occupied=False, room_id=self.id).first()
        seat.is_occupied = True
        seat.save()
        room = seat.room
        room.current_student_count += 1
        room.save()
        seat_history = SeatHistory.objects.create(
            student_id=student_id, seat_id=seat.id, filled_at=timezone.now()
        )
        return seat_history


class Seat(Timestampedmodel):
    name = models.CharField(max_length=64, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    is_occupied = models.BooleanField(default=False)


class SeatHistory(Timestampedmodel):
    seat = models.ForeignKey(Seat, on_delete=models.DO_NOTHING)
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    filled_at = models.DateTimeField(default=timezone.now)
    vacant_at = models.DateTimeField(null=True, blank=True)

    @transaction.atomic
    def remove_student(self):
        self.vacant_at = timezone.now()
        self.save()
        seat = self.seat
        seat.is_occupied = False
        seat.save()
        room = seat.room
        room.current_student_count -= 1
        room.save()
        return True

    def get_max_occupied_room(self):
        max_student_room_id = (
            Seat.objects.filter(vacant_at__isnull=False)
            .values("seat__room_id")
            .annotate(count=Count("id"))
            .order_by("count")
            .first()["seat__room_id"]
        )
        return {"room_id": max_student_room_id}
