from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from cars.views import CarsListView, NewCarCreateView, CarDetailView, CarUpdateView, CarDeleteView
from accounts.views import register_view, login_view, logout_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path(route='register/', view=register_view, name='register'),
    path(route='login/', view=login_view, name='login'),
    path(route='logout/', view=logout_view, name='logout'),
    path(route='cars/', view=CarsListView.as_view(), name='cars_list'),
    path(route='new_car/', view=NewCarCreateView.as_view(), name='new_car'),
    path(route='cars/<int:pk>/', view=CarDetailView.as_view(), name='car_detail'),
    path(route='cars/<int:pk>/update/', view=CarUpdateView.as_view(), name='car_update'),
    path(route='cars/<int:pk>/delete/', view=CarDeleteView.as_view(), name='car_delete'),
    path(route='', view=CarsListView.as_view(), name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not settings.DEBUG:
    from django.views.static import serve
    from django.urls import re_path

    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
