from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Watchlist
from auctions.models import Auction_listing
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.

@login_required
def watchlist(request, title):
    item = Auction_listing.objects.get(title=title)
    
    listing_exist = Watchlist.objects.filter(listing=item, user=request.user).exists()

    if not listing_exist:
        var = Watchlist(listing=item, user=request.user)
        var.save()
        return HttpResponseRedirect(reverse("watchlist"))
    
def display_Watchlist(request):
    context = {
        'items': Watchlist.objects.filter(user=request.user)
    }
    return render(request, 'user/displayWatchlist.html', context)

def deleteInWatchlist(request, id):
    item = Watchlist.objects.get(pk=id)
    item.delete()
    return HttpResponseRedirect(reverse("watchlist"))
