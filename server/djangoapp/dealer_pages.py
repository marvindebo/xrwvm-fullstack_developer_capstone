from django.http import HttpResponse
from django.utils.html import escape
from urllib.request import urlopen
import json

def kansas_dealers(request):
    try:
        with urlopen("http://127.0.0.1:3030/fetchDealers/Kansas", timeout=5) as response:
            dealers = json.load(response)
    except Exception:
        return HttpResponse("Dealership service unavailable", status=503)

    rows = "".join(
        f"<tr><td>{escape(str(d.get('id', '')))}</td>"
        f"<td>{escape(str(d.get('full_name', '')))}</td>"
        f"<td>{escape(str(d.get('city', '')))}</td>"
        f"<td>{escape(str(d.get('state', '')))}</td></tr>"
        for d in dealers
    )

    return HttpResponse(
        "<html><head><title>Kansas Dealerships</title></head>"
        "<body><h1>Dealerships in Kansas</h1>"
        "<table border='1' cellpadding='10'>"
        "<tr><th>ID</th><th>Dealership</th><th>City</th><th>State</th></tr>"
        + rows + "</table></body></html>"
    )
