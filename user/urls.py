from django.urls import path
from . import views

urlpatterns = [
    path("add-item-to-Watchlist/<str:title>", views.watchlist, name="addToWatchlist"),
    path("Watchlist", views.display_Watchlist, name="watchlist"),
    path("deleteItem/<int:id>", views.deleteInWatchlist, name="removeItem")
]
