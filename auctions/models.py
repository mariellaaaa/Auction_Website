from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    CATEGORY_CHOICES = [
        ('FASHION', 'Fashion'),
        ('TOYS', 'Toys'),
        ('ELECTRONICS', 'Electronics'),
        ('HOME', 'Home'),
        ('AUTOMOBILES', 'Automobiles'),
        ('BOOKS', 'Books'),
        ('ART', 'Art'),
        ('SPORT', 'Sport'),
        ('JEWERLY', 'Jewerly'),
        ('HANDMADE', 'Handmade'),
    ]

    title = models.CharField(max_length=40)
    description = models.TextField(max_length=300)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=200, blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    winning_bid = models.ForeignKey('Bid', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} bid {self.bid} on {self.listing}"

class Comment(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.listing}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="watchlisted_by")

    class Meta:
        unique_together = ("user", "listing")