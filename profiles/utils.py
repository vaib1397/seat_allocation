from django.db import transaction
from rest_framework.serializers import ValidationError
from profiles.models import Room, Seat, SeatHistory, Student


@transaction.atomic
def change_student_room(student_id, old_room_id, new_room_id):
    old_seat_history = SeatHistory.objects.filter(
        student_id=student_id, seat__room_id=old_room_id, vacant_at__isnull=True
    ).last()
    if not old_seat_history:
        raise ValidationError(
            f"Student is not present in given old room id: {old_room_id}"
        )
    old_seat_history.remove_student()

    room = Room.objects.get(id=new_room_id)
    if not room:
        raise ValidationError(f"No room found with given new room id: {new_room_id}")
    new_seat_history = room.add_student(student_id=student_id)
    return new_seat_history


def get_student_seat_on_given_date(student_id, date):
    student = Student.objects.get(id=student_id)
    seat = student.get_seat(date=date)
    return seat


def get_room_with_max_people():
    room = Room.objects.filter().order_by("current_student_count").last()
    return {"room_id": room.id}
