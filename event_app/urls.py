from . import views
from django.urls import path

urlpatterns = [
    # SIGNUP, LOGIN, AND LOGOUT
    path('', views.login, name='login'), # Root URL points to login
    path('signup/', views.register, name='signup'),  # Explicit signup URL
    path('logout/', views.logout_view, name='logout'),

    # DASHBOARDS
    path('index/', views.index, name='customer_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('theater_dashboard/', views.theater_dashboard, name='theater_dashboard'),

    #MOVIE CREATION,EDIT AND DELETE
    path('movie_create/', views.movie_create, name='movie_create'),
    path('movie/edit/<int:movie_id>/', views.edit_movie, name='edit_movie'),
    path('movie/delete/<int:movie_id>/',views.delete_movie, name='delete_movie'),
   #theater profile creation and updation
    path('theater/profile/create/', views.theater_profile_create, name='theater_profile_create'),
    path('theater/profile/update/', views.theater_profile_update, name='theater_profile_update'),
    
    #SHOW TIME MANAGEMENT
    path('showtime/add/', views.add_showtime, name='add_showtime'),
    path('showtime/edit/<int:showtime_id>/', views.edit_showtime, name='edit_showtime'),
    path('showtime/delete/<int:showtime_id>/', views.delete_showtime, name='delete_showtime'),

    #MOVIE DETAIL AND BOOKING
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
]
