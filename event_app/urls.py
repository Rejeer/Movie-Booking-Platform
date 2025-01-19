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
    path('booking/<int:movie_id>/',views.book_movie, name='book_movie'),
    #PAYMENT GATEWAY
    # path('payment/success/', views.payment_success, name='payment_success'),
    path('payment-success/', views.payment_success, name='payment_success'),
    # path('payment/failure/', views.payment_failure, name='payment_failure'),
    path('payment/<int:booking_id>/', views.payment_page, name='payment_page'),
    # path('process_payment/', views.process_payment, name='process_payment'),

    #ADMIN THEATER_LISTING
    path('theater_listing/',views.theater_list,name='theater_list'),
    path('theater/<int:id>/', views.theater_detail, name='theater_detail'),
    #TICKET
    path('ticket/<int:booking_id>/', views.view_ticket, name='view_ticket'),


    #CUSTOER PROFILE CREATIONS

    path('customer_profile/', views. customer_profile_create, name='customer_profile'),
    path('customer_view-profile/', views.customer_profile_view, name='customer_profile_view'),
 
    #CUSTOMER TICKET BOOKINGS
    path('customer/bookings/', views.customer_bookings, name='customer_bookings'),

    #TICKET RAISING AND LISTING
    path('raise_ticket/', views.raise_ticket, name='raise_ticket'),
    path('ticket_list/', views.ticket_list, name='ticket_list'),
    #HELPLINE FROM ADMINDASHBOARD
    path('help_line/', views.helpLine, name='help_line')
]
