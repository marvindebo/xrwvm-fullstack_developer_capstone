"""djangoproj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('djangoapp/', include('djangoapp.urls')),
    path('', TemplateView.as_view(template_name="Home.html")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


def dealership_list(request):
    import json
    from html import escape
    from urllib.request import urlopen
    from django.http import HttpResponse

    try:
        with urlopen("http://127.0.0.1:3030/fetchDealers", timeout=5) as response:
            dealers = json.load(response)
    except Exception as error:
        return HttpResponse("Dealership API unavailable", status=503)

    username = escape(request.user.username) if request.user.is_authenticated else ""
    status = (
        "<p><strong>Logged in as: " + username + "</strong></p>"
        if username else "<p>Not logged in</p>"
    )

    rows = ""
    for d in dealers:
        dealer_id = int(d["id"])
        review_link = (
            f'<a href="/dealer/{dealer_id}">Review Dealer</a>'
            if username else "Log in to review"
        )
        rows += (
            "<tr><td>" + str(dealer_id) + "</td><td>"
            + escape(str(d.get("full_name", "")))
            + "</td><td>" + escape(str(d.get("state", "")))
            + "</td><td>" + review_link + "</td></tr>"
        )

    return HttpResponse(
        "<h1>Dealerships</h1>"
        + status
        + "<table border='1' cellpadding='8'>"
        + "<tr><th>ID</th><th>Dealership</th><th>State</th>"
        + "<th>Action</th></tr>"
        + rows + "</table>"
    )

urlpatterns += [path("dealers", dealership_list)]

from djangoapp.dealer_pages import kansas_dealers
urlpatterns += [path("dealers/Kansas", kansas_dealers)]

from .dealer_detail_page import dealer_detail_page
urlpatterns += [path("dealer/<int:dealer_id>", dealer_detail_page)]

from .review_page import review_page
urlpatterns += [path("dealer/<int:dealer_id>/review", review_page)]
