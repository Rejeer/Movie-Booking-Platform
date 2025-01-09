from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
ROLE_CHOICES = [
    (1, 'Admin'),
    (2, 'Theater'),
    (3, 'Customer')
]

class CustomUserManager(BaseUserManager):
    def create_user(self, username=None, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        if not password:
            raise ValueError('The Password field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 1)
        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name='active')
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role = models.IntegerField(choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=True)

    # Avoiding reverse accessor conflicts
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_groups",
        blank=True,
        help_text="The groups this user belongs to."
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions",
        blank=True,
        help_text="Specific permissions for this user."
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username


    def __str__(self):
        return self.username

def __str__(self):
    return self.username

def is_admin(self):
    return self.role == 1

def is_theater(self):
    return self.role == 2

def is_customer(self):
    return self.role == 3

User=get_user_model()

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    duration = models.PositiveIntegerField()  # In minutes
    genre = models.CharField(max_length=100)
    language = models.CharField(max_length=50, default="English")
    poster = models.ImageField(upload_to='movies/posters/', null=True, blank=True)
    
    def __str__(self):
        return self.title
    



class Theater(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='theater_profile', null=True, blank=True)
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.TextField()
    capacity = models.IntegerField()
    contact_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.name

class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE,  related_name='showtimes')
    showtime = models.DateTimeField()

    def __str__(self):
        return f"{self.movie.title} - {self.theater.name} at {self.showtime}"
    

class Booking(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    number_of_tickets = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)


    def __str__(self):
        return f"{self.customer.username} - {self.movie.title} - {self.showtime.showtime}"