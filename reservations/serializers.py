
# reservations/serializers.py
from rest_framework import serializers
from .models import Room, Table, Reservation
from django.utils import timezone
from django.utils.timezone import localtime


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
    table_detail = TableSerializer(source='table', read_only=True)  # Read-only nested detail

    table = serializers.PrimaryKeyRelatedField(queryset=Table.objects.all())  # For writes
    

    class Meta:
        model = Reservation
        fields = '__all__'  # Or list fields explicitly if you prefer
        # optional: include table_detail in fields if you're not using '__all__'
    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Replace UTC datetimes with localized versions
        data['start_time'] = localtime(instance.start_time).strftime('%Y-%m-%d %H:%M:%S')
        data['end_time'] = localtime(instance.end_time).strftime('%Y-%m-%d %H:%M:%S')
        data['created_at'] = localtime(instance.created_at).strftime('%Y-%m-%d %H:%M:%S')

        return data
    
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
