# app/views.py
from django.conf import settings
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serialisers import EmailSerializer, EmailSerializerQuotation

 # Debugging line to check URL patterns
from rest_framework.views import APIView
from rest_framework.response import Response
from django.urls import URLPattern, URLResolver


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
        data = request.data
        print(data)
        serializer = EmailSerializer(data=request.data)


        if serializer.is_valid():
            subject = "QUOTATION REQUEST"
            message = serializer.validated_data["message"]
            from_email = settings.DEFAULT_FROM_EMAIL
            to = ["deadryefield@gmail.com"]

            try:
                send_mail(
                    subject,
                    message,
                    from_email,
                    to,
                    fail_silently=False,
                )
                return Response(
                    {"success": "Email sent successfully."}, status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@method_decorator(ratelimit(key="ip", rate="5/m", block=True), name="post")
class SendEmailQuotationView(APIView):

    def post(self, request):
        print("works")
        print(request.data)

        serializer = EmailSerializerQuotation(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data

            subject = "QUOTATION REQUEST"

            message = f"""
            New Quotation Request

            Name: {data.get('name')}
            Email: {data.get('email')}
            Mobile: {data.get('mobile')}

            Address:
            {data.get('address')}

            Requirements:
            {data.get('requirements')}

            Delivery Date: {data.get('deliveryDate')}
            """

            from_email = settings.DEFAULT_FROM_EMAIL
            to = ["deadryefield@gmail.com"]

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