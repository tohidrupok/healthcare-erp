from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect("dashboard")

    return render(request, "accounts/register.html")




def login_view(request):
    form = AuthenticationForm()  # this is important!

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid credentials")

    return render(request, "accounts/login.html", {"form": form})



# def login_view(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")

#         user = authenticate(request, username=username, password=password)
#         if user:
#             login(request, user)
#             return redirect("dashboard")
#         else:
#             messages.error(request, "Invalid credentials")

#     return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")




# from django.contrib.auth.forms import AuthenticationForm

# def login_view(request):
#     form = AuthenticationForm()

#     if request.method == "POST":
#         form = AuthenticationForm(request, data=request.POST)

#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect("dashboard")
#         else:
#             messages.error(request, "Invalid credentials")

#     return render(request, "accounts/login.html", {"form": form})



