from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import User, AuctionListing, Bid, Comment, Watchlist
from .forms import AuctionListingForm, BidForm, CommentForm


def index(request):
    active_listings = AuctionListing.objects.filter(active=True)

    for listing in active_listings:
        if listing.current_price is None:
            listing.current_price = listing.starting_bid
    return render(request, "auctions/index.html", {
        "active_listings": active_listings
    })

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

@login_required
def add_listing(request):
    if request.method == 'POST':
        form = AuctionListingForm(request.POST)
        if form.is_valid():
            auction_listing = form.save(commit=False)
            auction_listing.created_by = request.user
            auction_listing.save()

            return redirect("index")
    else:
        form = AuctionListingForm()

    return render(request, "auctions/add_listing.html", {
        "form": form
    })

def categories(request):
    categories = [choice[0] for choice in AuctionListing.CATEGORY_CHOICES]
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category_listing(request, category):
    listings = AuctionListing.objects.filter(category=category, active=True)
    return render(request, "auctions/category_listing.html", {
        "category": category,
        "listings": listings
    })

def watchlist(request):
    return render(request, "auctions/watchlist.html")

def listing_details(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)

    if listing.current_price is None:
        listing.current_price = listing.starting_bid

    form = BidForm()
    comment_form = CommentForm()
    error_message = None
    success_message = None

    if not listing.active:
        if listing.winning_bid:
            if request.user == listing.winning_bid.user:
                success_message = "This auction has been closed and you are the winner."
            elif request.user == listing.created_by:
                success_message = f"You have closed this auction. The winner is {listing.winning_bid.user.username}."
            else:
                success_message = "This auction is no longer available, the author has closed it."
        else:
            success_message = "This auction is no longer available, the author has closed it."

    if request.method == 'POST':
        if 'bid' in request.POST:
            form = BidForm(request.POST)
            if form.is_valid():
                bid = form.cleaned_data['bid']
                if bid > listing.current_price:
                    listing.current_price = bid
                    listing.save()

                    new_bid = Bid(user=request.user, listing=listing, bid=bid)
                    new_bid.save()

                    success_message_bid = "You have successfully placed your bid!"
                    return render(request, "auctions/listing_details.html", {
                        "listing": listing,
                        "form": form,
                        "comment_form": comment_form,
                        "comments": Comment.objects.filter(listing=listing).order_by('-created_at'),
                        "is_watchlisted": request.user.is_authenticated and Watchlist.objects.filter(user=request.user, listing=listing).exists(),
                        "error_message": error_message,
                        "success_message_bid": success_message_bid,
                        "number_of_bids": listing.bids.count(),
                    })
                else:
                    error_message = "Bid must be greater than the current price."
            else:
                error_message = "Invalid bid."
        elif 'comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.listing = listing
                comment.user = request.user
                comment.save()
                return HttpResponseRedirect(reverse('listing_details', args=[listing_id]))

        elif 'watchlist' in request.POST:
            if request.user.is_authenticated:
                if Watchlist.objects.filter(user=request.user, listing=listing).exists():
                    Watchlist.objects.filter(user=request.user, listing=listing).delete()
                else:
                    Watchlist.objects.create(user=request.user, listing=listing)
                return redirect('listing_details', listing_id=listing_id)

    comments = Comment.objects.filter(listing=listing).order_by('-created_at')
    is_watchlisted = request.user.is_authenticated and Watchlist.objects.filter(user=request.user, listing=listing).exists()

    return render(request, "auctions/listing_details.html", {
        "listing": listing,
        "form": form,
        "comment_form": comment_form,
        "comments": comments,
        "error_message": error_message,
        "is_watchlisted": is_watchlisted,
        "success_message": success_message,
        "number_of_bids": listing.bids.count(),
    })

@login_required
def watchlist(request):
    if request.method == 'POST':
        listing_id = request.POST.get('listing_id')
        listing = AuctionListing.objects.get(id=listing_id)
        watchlist_entry = Watchlist.objects.get(user=request.user, listing=listing)
        if 'remove' in request.POST:
            watchlist_entry.delete()
        return redirect('watchlist')

    watchlist_entries = Watchlist.objects.filter(user=request.user)
    watchlist = [entry.listing for entry in watchlist_entries]

    return render(request, 'auctions/watchlist.html', {
        'watchlist': watchlist
    })

@login_required
def close_auction(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)

    if request.user == listing.created_by:
        if listing.bids.exists():
            winning_bid = listing.bids.order_by('-bid').first()
            listing.winning_bid = winning_bid
            listing.active = False
            listing.save()
        else:
            error_message = f"There are no bids on '{listing.title}'. The auctions cannot be closed without any bids."
            messages.warning(request, error_message)
    else:
        error_message = "You are not authorized to close this auction."
        messages.warning(request, error_message)

    return redirect(reverse('listing_details', args=[listing_id]))

def closed_listings(request):
    closed_listings = AuctionListing.objects.filter(active=False)
    return render(request, "auctions/closed_listings.html", {
        "closed_listings": closed_listings
    })



        