from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add", views.add_listing, name="add_listing"),
    path("categories", views.categories, name="categories"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listing_details/<int:listing_id>/", views.listing_details, name="listing_details"),
    path("category_listing/<str:category>/", views.category_listing, name="category_listing"),
    path("close_auction/<int:listing_id>/", views.close_auction, name="close_auction"),
    path("closed_listings", views.closed_listings, name="closed_listings"),
]
