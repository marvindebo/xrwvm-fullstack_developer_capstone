# Uncomment the imports before you add the code
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    path('getallcarmakes', views.get_all_car_makes, name='getallcarmakes'),
    path('dealer/<int:dealer_id>/reviews', views.get_dealer_reviews),
    path('dealer/<int:dealer_id>', views.get_dealer_details),
    path('dealers/<str:state>', views.get_dealerships),
    path('dealers', views.get_dealerships),
    path('register', views.registration, name='register'),
    # # path for registration

    # path for login
    path('login', views.login_user, name='login'),
    path('logout', views.logout_request, name='logout'),

    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
