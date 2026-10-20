from django.urls import path

from . import views

urlpatterns = [
    # HTML pages
    path("", views.home, name="home"),
    path("about", views.about, name="about"),
    path("contact", views.contact, name="contact"),
    path("login", views.login_page, name="login_page"),
    path("logout", views.logout_page, name="logout_page"),
    path("register", views.register_page, name="register_page"),
    path("dealer/<int:dealer_id>", views.dealer_detail, name="dealer_detail"),
    path("dealer/<int:dealer_id>/review", views.post_review, name="post_review"),

    # JSON API endpoints
    path("djangoapp/get_dealers/", views.get_dealers, name="get_dealers"),
    path("djangoapp/get_dealers/<str:state>", views.get_dealers_by_state, name="get_dealers_by_state"),
    path("djangoapp/dealer/<int:dealer_id>", views.get_dealer_by_id, name="get_dealer_by_id"),
    path("djangoapp/reviews/dealer/<int:dealer_id>", views.get_dealer_reviews, name="get_dealer_reviews"),
    path("djangoapp/get_cars/", views.get_cars, name="get_cars"),
    path("djangoapp/analyze/<str:text>", views.analyze_review, name="analyze_review"),
    path("djangoapp/login", views.login_user, name="login_user"),
    path("djangoapp/logout", views.logout_user, name="logout_user"),
    path("djangoapp/register", views.register_user, name="register_user"),
]
