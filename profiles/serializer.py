from rest_framework.serializers import ValidationError
from rest_framework import serializers
from profiles.models import *
from profiles.utils import change_student_room


class ChangeRoomSerializer(serializers.Serializer):
    old_room_id = serializers.IntegerField()
    new_room_id = serializers.IntegerField()
    student_id = serializers.IntegerField()

    def create(self, validated_data):
        old_room_id = validated_data["old_room_id"]
        new_room_id = validated_data["new_room_id"]
        student_id = validated_data["student_id"]
        new_seat_history = change_student_room(
            student_id=student_id, old_room_id=old_room_id, new_room_id=new_room_id
        )
        return new_seat_history


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        exclude = ("created_at", "updated_at")


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        exclude = ("created_at", "updated_at")


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        exclude = ("created_at", "updated_at")

    def validate(self, data):
        current_student_count = data.get("current_student_count")
        if current_student_count != 0:
            raise ValidationError("You can't provide current student count, put it 0")
        return data

    def create(self, validated_data):
        room = super().create(validated_data)
        capacity = validated_data.get("capacity")
        if capacity:
            for i in range(capacity):
                room.add_seat()
        return room


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        exclude = ("created_at", "updated_at")


class SeatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SeatHistory
        exclude = ("created_at", "updated_at")
