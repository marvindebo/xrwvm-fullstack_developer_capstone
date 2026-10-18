
import json
from html import escape
from urllib.request import urlopen
from django.http import HttpResponse

def dealer_detail_page(request, dealer_id):
    try:
        with urlopen(f"http://127.0.0.1:3030/fetchDealer/{dealer_id}", timeout=10) as r:
            dealer = json.load(r)
        with urlopen(f"http://127.0.0.1:3030/fetchReviews/dealer/{dealer_id}", timeout=10) as r:
            reviews = json.load(r)
    except Exception as error:
        return HttpResponse(f"Dealer API unavailable: {escape(str(error))}", status=503)

    if not dealer:
        return HttpResponse("Dealer not found", status=404)

    html = "<h1>" + escape(str(dealer.get("full_name", "Dealership"))) + "</h1>"
    html += "<h2>Dealer Details</h2>"
    for key in ("id", "address", "city", "state", "zip"):
        html += "<p><b>" + escape(key.title()) + ":</b> " + escape(str(dealer.get(key, ""))) + "</p>"

    if request.user.is_authenticated:
        html += "<p><b>Logged in as: " + escape(request.user.username) + "</b></p>"
        html += f'<p><a href="/dealer/{dealer_id}/review">Review Dealer</a></p>'

    html += "<h2>Customer Reviews (" + str(len(reviews)) + ")</h2>"
    for review in reviews:
        html += "<div style='border:1px solid #ccc;padding:12px;margin:8px 0'>"
        html += "<b>" + escape(str(review.get("name", "Customer"))) + "</b>"
        html += "<p>" + escape(str(review.get("review", ""))) + "</p></div>"

    return HttpResponse(html)
