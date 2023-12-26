from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import *
from user.models import Watchlist
import pdb
from user.models import Watchlist
from django.contrib import messages
def index(request):
    listings = Auction_listing.objects.all()
    any_closed = False
    closed = []
    open = []
    for listing in listings:
        if listing.status == 'CLOSED':
            any_closed = True
            closed.append(listing)
        else:
            open.append(listing)

    context = {
        'open': open,
        'closed': closed,
        'any_closed': any_closed
    }
    """ Alternative
        open_listings = Auction_listing.objects.filter(status='OPEN')
        closed_listings = Auction_listing.objects.filter(status='CLOSED')

        context = {
            'open_listings': open_listings,
            'closed_listings': closed_listings
        }
    """
    return render(request, "auctions/index.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

class CreateListing(forms.Form):
    categories = Category.objects.all()

    title = forms.CharField(max_length=255, required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)
    price = forms.FloatField(required=True)
    image = forms.URLField(required=False)
    category = forms.ModelChoiceField(queryset=categories, required=True)


def create_listing(request):
    
    if request.method == "POST":
        form = CreateListing(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            price = form.cleaned_data.get('price')
            category = form.cleaned_data.get('category')
            image = form.cleaned_data.get('image')
            user = request.user

            
            var = Auction_listing(title=title, description=description, category=category, start_bid=price, image=image, user=user)
            var.save()
            
            return HttpResponseRedirect(reverse("index"))
        

    return render(request, 'auctions/create_listing.html', {"form": CreateListing()})

def display_listing(request, title):
    listing = Auction_listing.objects.get(title=title)
    comments = Comments.objects.filter(listing=listing)
    if listing.status == 'CLOSED':
        return HttpResponseRedirect(reverse('index'))
    bids = Bids.objects.filter(listing=listing)
    highest_bid = bids.order_by('-amount').first()

    lister = request.user == listing.user

    context = {
        "listing": listing,
        "listing_exist": Watchlist.objects.filter(listing = listing),
        "bid": highest_bid,
        "lister": lister,
        "comments": comments
    }

    return render(request, 'auctions/display_listing.html', context)


@login_required
def bid(request, title):
    listing_bid = Auction_listing.objects.filter(title=title).first()
    bid_exists = Bids.objects.filter(listing=listing_bid).exists()
    bids = Bids.objects.filter(listing=listing_bid)
    highest_bid = bids.order_by('-amount').first()
    # count = 0
    # for x in bids:
    #     if x.amount > count:
    #         count = x.amount
    #         highest_bid = x

    if request.method =="POST":
        bid = float(request.POST["bid"])
        if bid > listing_bid.start_bid:
            if bid_exists:
                if bid > highest_bid.amount:
                    highest_bid.amount = bid
                    
              
                    highest_bid.bidder = request.user
                    highest_bid.save()
                else:
                    messages.warning(request, f"The bid is lesser than the current bid")
                    return HttpResponseRedirect(reverse("displaylisting", args=(title,)))
            else:
                var = Bids(amount=bid, bidder=request.user, listing=listing_bid)
                var.save()
        else:
            messages.warning(request, f"The bid is lesser than the starting bid")
            return HttpResponseRedirect(reverse("displaylisting", args=(title,)))

    return HttpResponseRedirect(reverse("displaylisting", args=(title,)))

def close__Listing(request, id):
    listing = Auction_listing.objects.get(id=id)
    listing.status = "CLOSED"
    listing.save()

    watchlists = Watchlist.objects.all()
    for watchlist in watchlists:
        if watchlist.listing.status == "CLOSED":
            watchlist.delete()


    return HttpResponseRedirect(reverse("index"))

def comments(request, title):
    listing = Auction_listing.objects.get(title=title)
    if request.method == "POST":
        comment = request.POST['comment']
        var = Comments(comment=comment, listing=listing ,user=request.user)
        var.save()

    return HttpResponseRedirect(reverse("displaylisting", args=(title,)))

def display_category(request):

    context = {
        'categories': Category.objects.all()
    }

    return render(request, 'auctions/category.html', context)

def category_item(request, id):
    listings = Auction_listing.objects.filter(category=id)
    category = Category.objects.get(id=id)
    context = {
        'listings': listings,
        'category': category
    }

    return render(request, 'auctions/category_item.html', context)