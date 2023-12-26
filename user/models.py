from django.db import models
from auctions.models import Auction_listing, User

# Create your models here.
class Watchlist(models.Model):
    listing = models.ForeignKey(Auction_listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Item '{self.listing.title}' In Watchlist of {self.user}"