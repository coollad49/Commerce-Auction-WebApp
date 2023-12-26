from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Auction_listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_bid = models.FloatField(max_length=100)
    image = models.URLField()
    date = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=10, default="OPEN")

    def __str__(self):
        return f"Auction for {self.title}"


class Bids(models.Model):
    amount = models.FloatField(max_length=100)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Auction_listing, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"Bid for {self.listing.title}"
    
    class Meta:
        verbose_name_plural = "Bids"

class Comments(models.Model):
    comment = models.TextField()
    listing = models.ForeignKey(Auction_listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment on {self.listing.title} by {self.user}"
    
    class Meta:
        verbose_name_plural = "Comments"