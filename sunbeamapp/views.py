# app/views.py
from django.conf import settings
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_ratelimit.exceptions import Ratelimited
from .serialisers import EmailSerializer, EmailSerializerQuotation

 # Debugging line to check URL patterns

import os
from django.urls import URLPattern, URLResolver

from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    if isinstance(exc, Ratelimited):
        return Response(
            {"error": "Too many requests"},
            status=status.HTTP_429_TOO_MANY_REQUESTS
        )
    return exception_handler(exc, context)

class APIRootView(APIView):

    def get(self, request):
        from .urls import urlpatterns

        def extract_urls(patterns, prefix=""):
            endpoints = {}

            for pattern in patterns:
                if isinstance(pattern, URLPattern):
                    name = pattern.name or str(pattern.pattern)
                    path = prefix + str(pattern.pattern)
                    endpoints[name] = f"/{path}"

                elif isinstance(pattern, URLResolver):
                    # nested urls
                    endpoints.update(
                        extract_urls(pattern.url_patterns, prefix + str(pattern.pattern))
                    )

            return endpoints

        endpoints = extract_urls(urlpatterns)

        return Response({
            "message": "Welcome to SunBeam Digi API",
            "version": "1.0",
            "endpoints": endpoints
        })

@method_decorator(ratelimit(key="ip", rate="5/m", block=True), name="post")
class SendEmailView(APIView):
    serializer_class = EmailSerializer

    def post(self, request):
        print("works")
        print(request.data)

        serializer = EmailSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data

            subject = data.get("subject") or "Form Submission"

            message = f"""
                New Form Submission

                Name: {data.get('name')}
                Email: {data.get('email')}
                Mobile: {data.get('mobile')}

                Message:
                {data.get('message')}
                """

            from_email = settings.DEFAULT_FROM_EMAIL
            to = data.get("to") or [os.getenv("EMAIL_TO")]

            try:
                send_mail(
                    subject,
                    message,
                    from_email,
                    to,
                    fail_silently=False,
                )
                return Response(
                    {"success": "Email sent successfully."},
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@method_decorator(ratelimit(key="ip", rate="5/m", block=True), name="post")
class SendEmailQuotationView(APIView):

    def post(self, request):
        print("works")
        print(request.data)
        data = request.data.copy()  # IMPORTANT: make it mutable

        # 🔥 FIX: convert empty string to None BEFORE serializer
        if data.get("deadline") == "":
            data["deadline"] = None

        serializer = EmailSerializerQuotation(data=data)

        if serializer.is_valid():
            data = serializer.validated_data

            subject = "QUOTATION REQUEST"

            message = f"""
            New Quotation Request

            Name: {data.get('name')}
            Email: {data.get('email')}
            Phone: {data.get('phone')}

            Project: {data.get('project')}
            Quantity: {data.get('quantity')}
            Size: {data.get('size')}

            Details:
            {data.get('details')}

            Deadline: {data.get('deadline')}
            """
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email =os.getenv("EMAIL_TO")
            to = [to_email]

            try:
                send_mail(
                    subject,
                    message,
                    from_email,
                    to,
                    fail_silently=False,
                )
                return Response(
                    {"success": True}, status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        print(serializer.errors)  # 👈 VERY IMPORTANT for debugging
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)