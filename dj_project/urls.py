from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from products.views import (CancelView, CreateCheckoutSessionView,
                            ProductLandingPageView, StripeIntentView,
                            SuccessView, stripe_webhook)

schema_view = get_schema_view(
    openapi.Info(
        title='Project name',
        default_version='v1',
        description='API for ...',
        contact=openapi.Contact(email='vasya@mail.ru'),
        license=openapi.License(name=''),
    ),
    # url='http://127.0.0.1:8000',
    public=True,
    permission_classes=(permissions.AllowAny, permissions.IsAuthenticated),
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('create-payment-intent/<pk>/', StripeIntentView.as_view(), name='create-payment-intent'),
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path('', ProductLandingPageView.as_view(), name='landing-page'),
    path('', include('products.urls')),
    path('create-checkout-session/<pk>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('api/v1/', include('rest_basics.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('swagger(format\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
