from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CustomTokenObtainPairView, FlipBookViewSet, flipbook_view, get_authenticated_user, protected_view, register_user
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r"flipbooks", FlipBookViewSet, basename="flipbook")

urlpatterns = [
    path("api/register/", register_user, name="register"),
    path("api/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/", include(router.urls)),
    path('flipbook/<int:flipbook_id>/', flipbook_view, name='flipbook_view'),
    path("api/user/", get_authenticated_user, name="authenticated_user"),
    path('api/protected/', protected_view, name='protected'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)