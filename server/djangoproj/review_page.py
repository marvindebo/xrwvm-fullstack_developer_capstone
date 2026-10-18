import json
from html import escape
from urllib.request import Request, urlopen

from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect


@login_required(login_url="/admin/login/")
@csrf_protect
def review_page(request, dealer_id):
    if request.method == "POST":
        data = {
            "name": request.user.username,
            "dealership": dealer_id,
            "review": request.POST.get("review", ""),
            "purchase": request.POST.get("purchase") == "on",
            "purchase_date": request.POST.get("purchase_date", ""),
            "car_make": request.POST.get("car_make", ""),
            "car_model": request.POST.get("car_model", ""),
            "car_year": int(request.POST.get("car_year") or 2023),
        }

        if not data["review"].strip():
            return HttpResponse("Review text is required", status=400)

        req = Request(
            "http://127.0.0.1:3030/insert_review",
            data=json.dumps(data).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urlopen(req, timeout=10) as response:
                result = json.load(response)
        except Exception as error:
            return HttpResponse(
                "Review submission failed: " + escape(str(error)),
                status=502,
            )

        if not result.get("id"):
            return HttpResponse("Review was not confirmed", status=502)

        return redirect("/dealer/" + str(dealer_id))

    from django.middleware.csrf import get_token

    token = escape(get_token(request))

    return HttpResponse(f"""
    <html>
    <head><title>Review Dealer</title></head>
    <body>
    <h1>Submit a Dealership Review</h1>
    <h2>Dealer ID: {dealer_id}</h2>
    <p>Logged in as: {escape(request.user.username)}</p>

    <form method="post">
      <input type="hidden" name="csrfmiddlewaretoken" value="{token}">

      <p>Review:<br>
      <textarea name="review" rows="5" cols="55" required></textarea></p>

      <p><label>
      <input type="checkbox" name="purchase">
      Purchased a vehicle
      </label></p>

      <p>Purchase Date:
      <input type="date" name="purchase_date"></p>

      <p>Car Make:
      <input name="car_make" value="Nissan"></p>

      <p>Car Model:
      <input name="car_model" value="Pathfinder"></p>

      <p>Car Year:
      <input type="number" name="car_year" value="2023"></p>

      <button type="submit">Submit Review</button>
    </form>
    </body>
    </html>
    """)
