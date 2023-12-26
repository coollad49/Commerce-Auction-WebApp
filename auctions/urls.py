from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.create_listing, name="createlisting"),
    path("listings/<str:title>", views.display_listing, name="displaylisting"),
    path("Bid/<str:title>", views.bid, name="bids"),
    path("CloseListing/<int:id>", views.close__Listing, name="closeListing"),
    path("comments/<str:title>", views.comments, name="comment"),
    path("Categories", views.display_category, name="category"),
    path("Categories/<int:id>", views.category_item, name="categoryItem"),
]
