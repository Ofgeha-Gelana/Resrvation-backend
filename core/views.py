from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SummaryRequestSerializer
from .utils import search_duckduckgo, call_open_llm_api
from rest_framework.permissions import AllowAny

class GetSummaryView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = SummaryRequestSerializer(data=request.data)
        if serializer.is_valid():
            company = serializer.validated_data['company_name']
            # employee = serializer.validated_data['employee_name']
            # employee = serializer.validated_data['employee_name']
            employee = serializer.validated_data.get('employee_name') or []

            query = f"{company} {employee} role"
            web_data = search_duckduckgo(query)

            prompt = f"""
            Based on this web search information, summarize in one paragraph what the company '{company}' does and the role of employee '{employee}' in the company, do this for all lists employee provided. i don't need to know the employee name in the company summary: 
            {web_data}
            """
            print("employee", employee)
            summary = call_open_llm_api(prompt)
            return Response(summary)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
