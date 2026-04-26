from django.urls import path
from .views import SendEmailView, APIRootView, SendEmailQuotationView
urlpatterns = [
    # path("admin/", admin.site.urls),
    # path('api-auth/', include('rest_framework.urls')),
    path("", APIRootView.as_view(), name="api-root"),
    path("contact-form/", SendEmailView.as_view() ),
    path("quotation-form/", SendEmailQuotationView.as_view() )
]
