from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('finder/', views.meal_finder, name='meal_finder'),
    path('results/', views.meal_results, name='meal_results'),
    path('meal/<int:meal_id>/', views.meal_detail, name='meal_detail'),  # FIXED
    path('meal/<int:meal_id>/save/', views.save_meal, name='save_meal'),  # FIXED
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)