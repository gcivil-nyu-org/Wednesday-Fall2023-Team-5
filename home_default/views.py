from django.shortcuts import render


# Create your views here.
def home_page(request):
    return render(request, "home_default/home.html", {})


def custom_403(request, exception):
    return render(request, 'home_default/403.html', {}, status=403)
