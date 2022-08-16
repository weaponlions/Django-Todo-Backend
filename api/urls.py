from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView, TokenRefreshView
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('notes', views.NotesViewSet)

urlpatterns = [
    path('notes/registration/', views.SignUpApi.as_view()),
    # path('notes/registration/', views.SignUpApi.as_view()),
    path('notes/login/', views.SignInApi.as_view()),
    # path('notes/token/', TokenObtainPairView.as_view(), name='token_obtain_pair', ),
    # path('notes/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # path('notes/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
