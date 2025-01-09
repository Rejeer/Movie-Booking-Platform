from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse, Http404
from django.contrib.auth import authenticate,logout, login as auth_login
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
import random
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Movie, Theater, Showtime, Booking
import random
from django.db.models import Sum
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Movie, Theater, Showtime, Booking
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Movie, Theater, Showtime, Booking
from django.db.models import Sum
import random
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test
# Custom User Creation Form
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Redirect based on user role
            if user.role == 1:  # Admin
                return redirect('admin_dashboard')
                
            elif user.role == 2:  # Company
                return redirect('theater_dashboard')
            elif user.role == 3:  # Applicant
                return redirect('customer_dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login(request):
    next_url = request.GET.get('next', '/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if user.role == 1:  # Admin
                return redirect('admin_dashboard')
            elif user.role == 2:  # Company
                return redirect('theater_dashboard')
            elif user.role == 3:  # Applicant
                return redirect('customer_dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html', {'next': next_url})


def logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('login') 


@login_required
def index(request):
    movies = Movie.objects.all()
    bookings = Booking.objects.filter(customer=request.user)
    return render(request, 'index.html', {'movies': movies , 'bookings': bookings})


@login_required
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    return render(request, 'movie_detail.html', {'movie': movie})

@login_required
def admin_dashboard(request):
    movies = Movie.objects.all()
    theater = Theater.objects.all()
    return render(request, 'admin_dashboard.html' ,{'movies': movies,'theater':theater})


@login_required
def theater_list(request):
    theater = Theater.objects.all()  # Get all theaters
    return render(request, 'theater_list.html', {'theater': theater})

@login_required
def theater_detail(request, id):
    theater = Theater.objects.get(id=id)
    showtimes = Showtime.objects.filter(theater=theater)  # Get the theater by ID
    return render(request, 'theater_detail.html', {'theater': theater,'showtimes': showtimes})

@login_required
# def theater_dashboard(request):
#     # Check if a theater profile exists for the logged-in user
#     theater_exists = Theater.objects.filter(user=request.user).exists()

#     if theater_exists:
#         theater = Theater.objects.get(user=request.user)  # Get the theater linked to the user
#         showtimes = Showtime.objects.filter(theater=theater)  # Fetch related showtimes
#     else:
#         theater = None
#         showtimes = None

#     return render(request, 'theater_dashboard.html', {
#         'theater_exists': theater_exists,
#         'theater': theater,
#         'showtimes': showtimes,
#     })


def theater_dashboard(request):
    # Check if a theater profile exists for the logged-in user
    theater_exists = Theater.objects.filter(user=request.user).exists()

    if theater_exists:
        theater = Theater.objects.get(user=request.user)  # Get the theater linked to the user
        showtimes = Showtime.objects.filter(theater=theater)  # Fetch related showtimes
        bookings = Booking.objects.filter(theater=theater)  # Fetch bookings for this theater
    else:
        theater = None
        showtimes = None
        bookings = None

    return render(request, 'theater_dashboard.html', {
        'theater_exists': theater_exists,
        'theater': theater,
        'showtimes': showtimes,
        'bookings': bookings,
    })

def movie_create(request):
    if request.method == 'POST':
        # Get form data
        title = request.POST.get('title')
        description = request.POST.get('description')
        duration = request.POST.get('duration')  # Duration in minutes
        release_date = request.POST.get('release_date')
        poster = request.FILES.get('poster')  # For file upload (poster)

        # Create the movie object
        movie = Movie.objects.create(
            title=title,
            description=description,
            duration=duration,
            release_date=release_date,
            poster=poster
        )

        # Redirect to movie list or another page after creation
        return redirect('admin_dashboard')  # Change 'movie_list' to your desired URL name

    # Render the movie creation form
    return render(request, 'movie_create.html')


@login_required
def edit_movie(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    if request.method == 'POST':
        movie.title = request.POST.get('title')
        movie.description = request.POST.get('description')
        movie.duration = request.POST.get('duration')
        movie.release_date = request.POST.get('release_date')
        
        if 'poster' in request.FILES:
            movie.poster = request.FILES['poster']  # Update poster if provided
        
        movie.save()  # Save changes
        return redirect('admin_dashboard')  # Redirect to the movie list or another page

    return render(request, 'edit_movie.html', {'movie': movie})


@login_required
def delete_movie(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    if request.method == 'POST':
        movie.delete()
        return redirect('admin_dashboard')

    return render(request, 'delete_movie.html', {'movie': movie})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Theater
from django.contrib import messages

@login_required
def theater_profile_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        capacity = request.POST.get('capacity')
        contact_number = request.POST.get('contact_number')
        price = request.POST.get('price')  # Fetch the ticket price

        # Check if a profile already exists
        if Theater.objects.filter(user=request.user).exists():
            messages.error(request, 'Theater profile already exists!')
            return redirect('theater_dashboard')

        # Create the theater profile
        Theater.objects.create(
            user=request.user,
            name=name,
            location=location,
            capacity=capacity,
            contact_number=contact_number,
            price=price  # Save ticket price
        )
        messages.success(request, 'Theater profile created successfully!')
        return redirect('theater_dashboard')

    return render(request, 'theater_profile_create.html')



@login_required
def theater_profile_update(request):
    theater = Theater.objects.filter(user=request.user).first()
    if not theater:
        messages.error(request, 'No theater profile found!')
        return redirect('theater_profile_create')

    if request.method == 'POST':
        theater.name = request.POST.get('name')
        theater.location = request.POST.get('location')
        theater.capacity = request.POST.get('capacity')
        theater.contact_number = request.POST.get('contact_number')
        theater.price = request.POST.get('price')
        theater.save()
        messages.success(request, 'Theater profile updated successfully!')
        return redirect('theater_dashboard')

    return render(request, 'theater_profile_update.html', {'theater': theater})


def add_showtime(request):
    # Ensure the user has a theater profile
    try:
        theater = request.user.theater_profile
    except Theater.DoesNotExist:
        messages.error(request, 'Please create your theater profile first.')
        return redirect('theater_profile_create')

    if request.method == 'POST':
        movie_id = request.POST.get('movie')
        showtime = request.POST.get('showtime')

        movie = Movie.objects.get(id=movie_id)

        Showtime.objects.create(movie=movie, theater=theater, showtime=showtime)
        messages.success(request, 'Showtime added successfully!')
        return redirect('theater_dashboard')

    movies = Movie.objects.all()
    return render(request, 'add_showtime.html', {'movies': movies, 'theater': theater})


@login_required
def edit_showtime(request, showtime_id):
    showtime = Showtime.objects.get(id=showtime_id)

    # Ensure the logged-in user owns this theater
    if showtime.theater.user != request.user:
        messages.error(request, 'You are not authorized to edit this showtime.')
        return redirect('theater_dashboard')

    if request.method == 'POST':
        movie_id = request.POST.get('movie')
        new_showtime = request.POST.get('showtime')

        showtime.movie = Movie.objects.get(id=movie_id)
        showtime.showtime = new_showtime
        showtime.save()
        messages.success(request, 'Showtime updated successfully!')
        return redirect('theater_dashboard')

    movies = Movie.objects.all()
    return render(request, 'edit_showtime.html', {'showtime': showtime, 'movies': movies})


@login_required
def delete_showtime(request, showtime_id):
    showtime = Showtime.objects.get(id=showtime_id)

    # Ensure the logged-in user owns this theater
    if showtime.theater.user != request.user:
        messages.error(request, 'You are not authorized to delete this showtime.')
        return redirect('theater_dashboard')

    showtime.delete()
    messages.success(request, 'Showtime deleted successfully!')
    return redirect('theater_dashboard')







from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Movie, Theater, Showtime, Booking
from django.db.models import Sum

@login_required
def book_movie(request, movie_id):
    # Get the selected movie
    movie = get_object_or_404(Movie, id=movie_id)
    
    # Filter theaters and showtimes for this movie
    theaters = Theater.objects.filter(showtimes__movie=movie).distinct()
    showtimes = Showtime.objects.filter(movie=movie).distinct()

    if request.method == 'POST':
        # Retrieve form data
        theater_id = request.POST.get('theater')
        showtime_id = request.POST.get('showtime')
        number_of_tickets = request.POST.get('quantity')  # Assuming 'quantity' in HTML form

        # Validate user inputs
        if not theater_id or not showtime_id or not number_of_tickets:
            messages.error(request, "All fields are required.")
            return redirect('book_movie', movie_id=movie_id)

        # Get the theater and showtime objects
        theater = get_object_or_404(Theater, id=theater_id)
        showtime = get_object_or_404(Showtime, id=showtime_id)

        # Convert tickets to integer
        try:
            number_of_tickets = int(number_of_tickets)
        except ValueError:
            messages.error(request, "Please enter a valid number of tickets.")
            return redirect('book_movie', movie_id=movie_id)

        # Check theater capacity
        max_capacity = theater.capacity or 0
        tickets_booked = Booking.objects.filter(theater=theater, showtime=showtime).aggregate(
            total_tickets=Sum('number_of_tickets')
        )['total_tickets'] or 0
        available_tickets = max_capacity - tickets_booked

        if available_tickets <= 0:
            messages.error(request, "This show is sold out!")
            return redirect('book_movie', movie_id=movie_id)

        if number_of_tickets > available_tickets:
            messages.warning(request, f"Only {available_tickets} tickets are available. Booking adjusted.")
            number_of_tickets = available_tickets

        # Create booking entry
        booking = Booking.objects.create(
            customer=request.user,
            movie=movie,
            theater=theater,
            showtime=showtime,
            number_of_tickets=number_of_tickets
        )
        
        messages.success(request, "Your booking was successful!")
        return redirect('payment_page', booking_id=booking.id)

    context = {
        'movie': movie,
        'theaters': theaters,
        'showtimes': showtimes
    }
    return render(request, 'book_movie.html', context)








@login_required
def user_bookings(request, booking_id):
    # Get the booking details
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    movie_price = booking.movie.price * booking.quantity
    # Render the booking details in a separate template
    return render(request, 'booking.html', {'booking': booking,'movie_price': movie_price})



#PAYMENT GATEWAY
import hashlib
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
import requests

def payment_page(request, booking_id):
    """Render the payment page."""
    booking = get_object_or_404(Booking, id=booking_id)
    theater_price = booking.theater.price
    total_price = theater_price * booking.quantity
    return render(request, "payment.html", {'booking': booking, 'total_price': total_price})




def payment_success(request):
    return render(request, 'payment_success.html')