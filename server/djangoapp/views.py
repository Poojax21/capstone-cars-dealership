import json

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import CarMake, Dealer, Review

POSITIVE_WORDS = {
    "fantastic", "great", "excellent", "amazing", "good", "love", "loved",
    "awesome", "wonderful", "best", "happy", "satisfied", "perfect", "friendly",
    "helpful", "recommend", "nice", "superb", "outstanding", "pleasant", "easy",
}
NEGATIVE_WORDS = {
    "bad", "terrible", "awful", "poor", "worst", "hate", "hated", "horrible",
    "disappointed", "disappointing", "rude", "slow", "expensive", "overpriced",
    "dirty", "unprofessional", "angry", "unhappy", "problem", "issue", "waste",
}


def analyze_sentiment(text):
    """Simple lexicon based sentiment analysis.

    A remote Watson NLU service can be plugged in here; this local fallback keeps
    the endpoint deterministic and available offline.
    """
    words = [w.strip(".,!?;:\"'").lower() for w in text.split()]
    pos = sum(1 for w in words if w in POSITIVE_WORDS)
    neg = sum(1 for w in words if w in NEGATIVE_WORDS)
    if pos > neg:
        return "positive"
    if neg > pos:
        return "negative"
    return "neutral"


def _dealer_dict(dealer):
    return {
        "id": dealer.id,
        "full_name": dealer.full_name,
        "short_name": dealer.short_name,
        "address": dealer.address,
        "city": dealer.city,
        "state": dealer.state,
        "zip": dealer.zip,
        "latitude": dealer.latitude,
        "longitude": dealer.longitude,
    }


def _review_dict(review):
    return {
        "id": review.id,
        "name": review.name,
        "dealership": review.dealer_id,
        "review": review.review,
        "purchase": review.purchase,
        "purchase_date": review.purchase_date.isoformat() if review.purchase_date else None,
        "car_make": review.car_make,
        "car_model": review.car_model,
        "car_year": review.car_year,
        "sentiment": review.sentiment,
    }


# ---------------------------------------------------------------------------
# HTML pages
# ---------------------------------------------------------------------------
def home(request):
    state = request.GET.get("state", "")
    if state:
        dealers = Dealer.objects.filter(state__iexact=state).order_by("full_name")
    else:
        dealers = Dealer.objects.all().order_by("full_name")
    states = Dealer.objects.values_list("state", flat=True).distinct().order_by("state")
    return render(request, "home.html", {
        "dealers": dealers,
        "states": states,
        "selected_state": state,
        "logged_in": request.user.is_authenticated,
    })


def dealer_detail(request, dealer_id):
    dealer = get_object_or_404(Dealer, pk=dealer_id)
    reviews = dealer.reviews.all().order_by("-id")
    return render(request, "dealer.html", {
        "dealer": dealer,
        "reviews": reviews,
        "logged_in": request.user.is_authenticated,
    })


def post_review(request, dealer_id):
    dealer = get_object_or_404(Dealer, pk=dealer_id)
    if request.method == "POST":
        name = request.POST.get("name", request.user.username if request.user.is_authenticated else "Anonymous")
        text = request.POST.get("review", "")
        Review.objects.create(
            dealer=dealer,
            name=name,
            purchase=request.POST.get("purchase") == "on",
            review=text,
            sentiment=analyze_sentiment(text),
            car_make=request.POST.get("car_make", ""),
            car_model=request.POST.get("car_model", ""),
            car_year=request.POST.get("car_year", ""),
        )
        return redirect("dealer_detail", dealer_id=dealer.id)
    return render(request, "post_review.html", {
        "dealer": dealer,
        "logged_in": request.user.is_authenticated,
    })


def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("userName") or request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("home")
        return render(request, "login.html", {"error": "Invalid username or password"})
    return render(request, "login.html")


def logout_page(request):
    auth_logout(request)
    return redirect("home")


def register_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")
        email = request.POST.get("email", "")
        if username and password and not User.objects.filter(username=username).exists():
            User.objects.create_user(username=username, password=password,
                                     first_name=first_name, last_name=last_name,
                                     email=email)
            return redirect("login_page")
    return render(request, "register.html")


# ---------------------------------------------------------------------------
# JSON API endpoints (used by the cURL tasks)
# ---------------------------------------------------------------------------
def get_dealers(request):
    dealers = Dealer.objects.all().order_by("id")
    return JsonResponse({"status": 200, "dealers": [_dealer_dict(d) for d in dealers]})


def get_dealers_by_state(request, state):
    dealers = Dealer.objects.filter(state__iexact=state).order_by("id")
    return JsonResponse({"status": 200, "dealers": [_dealer_dict(d) for d in dealers]})


def get_dealer_by_id(request, dealer_id):
    dealer = get_object_or_404(Dealer, pk=dealer_id)
    return JsonResponse({"status": 200, "dealer": _dealer_dict(dealer)})


def get_dealer_reviews(request, dealer_id):
    dealer = get_object_or_404(Dealer, pk=dealer_id)
    reviews = dealer.reviews.all().order_by("id")
    return JsonResponse({
        "status": 200,
        "dealer": dealer.short_name,
        "reviews": [_review_dict(r) for r in reviews],
    })


def get_cars(request):
    makes = []
    for make in CarMake.objects.all().order_by("name"):
        models = [
            {"name": m.name, "type": m.type, "year": m.year}
            for m in make.models.all().order_by("name")
        ]
        makes.append({"make": make.name, "models": models})
    return JsonResponse({"status": 200, "car_makes": makes})


def analyze_review(request, text):
    return JsonResponse({
        "status": 200,
        "text": text,
        "sentiment": analyze_sentiment(text),
    })


@csrf_exempt
@require_http_methods(["POST"])
def login_user(request):
    username = request.POST.get("userName") or request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    if user is not None:
        auth_login(request, user)
        return JsonResponse({
            "status": 200,
            "message": "Login successful",
            "userName": user.username,
            "firstName": user.first_name,
            "lastName": user.last_name,
        })
    return JsonResponse({"status": 401, "message": "Invalid username or password"}, status=401)


@csrf_exempt
@require_http_methods(["POST", "GET"])
def logout_user(request):
    auth_logout(request)
    return JsonResponse({"status": 200, "message": "Logged out successfully"})


@csrf_exempt
@require_http_methods(["POST"])
def register_user(request):
    data = request.POST
    if not data and request.body:
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = {}
    username = data.get("username") or data.get("userName")
    password = data.get("password")
    if not username or not password:
        return JsonResponse({"status": 400, "message": "username and password required"}, status=400)
    if User.objects.filter(username=username).exists():
        return JsonResponse({"status": 409, "message": "User already exists"}, status=409)
    user = User.objects.create_user(
        username=username, password=password,
        first_name=data.get("first_name", ""),
        last_name=data.get("last_name", ""),
        email=data.get("email", ""),
    )
    return JsonResponse({"status": 200, "message": "Registration successful", "userName": user.username})
