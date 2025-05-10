
# reservations/serializers.py
from rest_framework import serializers
from .models import Room, Table, Reservation
from django.utils import timezone

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    tables = TableSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

    def validate(self, data):
        table = data['table']
        start = data['start_time']
        end = data['end_time']

        if start >= end:
            raise serializers.ValidationError("End time must be after start time.")

        if data['number_of_guests'] > table.capacity:
            raise serializers.ValidationError("Guest number exceeds table capacity.")

        overlapping = Reservation.objects.filter(
            table=table,
            start_time__lt=end,
            end_time__gt=start
        )
        if overlapping.exists():
            raise serializers.ValidationError("This table is already reserved for that time.")

        return data

