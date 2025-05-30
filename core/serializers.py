from rest_framework import serializers

class SummaryRequestSerializer(serializers.Serializer):
    company_name = serializers.CharField(label="Company Name", max_length=100)
    employee_name = serializers.CharField(
        label="Employee Name",
        required=False
    )