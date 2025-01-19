# utils.py
from django.core.mail import send_mail

def send_booking_confirmation_email(customer_email, movie_title, showtime, theater_name, tickets):
    subject = 'Your Movie Booking Confirmation'
    message = (
        f"Dear Customer,\n\n"
        f"Thank you for booking tickets with us!\n"
        f"Here are your booking details:\n\n"
        f"Movie: {movie_title}\n"
        f"Theater: {theater_name}\n"
        f"Showtime: {showtime}\n"
        f"Tickets: {tickets}\n\n"
        f"Enjoy your movie!\n\n"
        f"Best regards,\nMovie Booking Team"
    )
    send_mail(
        subject=subject,
        message=message,
        from_email='your_email@gmail.com',
        recipient_list=[customer_email],
        fail_silently=False,
    )
