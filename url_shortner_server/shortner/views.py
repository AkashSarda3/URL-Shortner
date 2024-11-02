"""Views module stores all the views of the application"""
from shortner.new_view import NewView
from shortner.stub_view import StubView
from shortner.delete_view import DeleteView
from shortner.list_view import ListUrlsView
from shortner.update_view import UpdateView
from shortner.custom_view import CustomView
from shortner.stats_view import StatsView
from shortner.login import login_test
from shortner.models import Link
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

__all__ = ["NewView", "StubView", "UpdateView", "DeleteView",
           "ListUrlsView", "login_test", "CustomView", "StatsView", "delete_all_urls"]


def home(request):
    """home view"""
    print("hitting home")
    return render(request, "authentication/index.html")


def signup(request):
    """signup view"""
    if request.method == "POST":
        # requestJsonBody = json.loads(request)
        uservalue = request.POST["username"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        password1 = request.POST["pass1"]
        password2 = request.POST["pass2"]

        if User.objects.filter(username=uservalue).exists():
            messages.error(request, "Username is already taken")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email is already used")
        elif len(email) < 4:
            messages.error(request, "Email must be greater \
                than 3 characters.")
        elif len(fname) < 2:
            messages.error(request, "First name must be \
                greater than 1 character.")
        elif len(lname) < 2:
            messages.error(request, "Last name must be \
                greater than 1 character.")
        elif password1 != password2:
            messages.error(request, "Passwords don't match.")
        elif len(password1) < 5:
            messages.error(request, "Password must be \
                at least 5 characters.")
        else:
            myuser = User.objects.create_user(uservalue, email, password1)
            myuser.first_name = fname
            myuser.last_name = lname

            myuser.save()
            messages.success(request, "Your Account has been \
                successfully created.")
            request.session['username'] = uservalue
            return redirect("home")
    return render(request, "authentication/signup.html")


def signin(request):
    """signin view"""

    # Only through forms
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["pass1"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            fname = user.first_name
            request.session['username'] = username
            return redirect("homepage", fname=fname)
        else:
            messages.error(request, "Bad Credentials!")
            return redirect("home")

    # Render the main page if we try to access signin through the url (GET)
    return render(request, "authentication/index.html")


def homepage(request, fname):
    """homepage view"""
    if (request.method == 'GET'):
        messages.success(request, "Login Successfull!")
        print(f"{fname} has logged in")
        args = {}
        args['userFname'] = fname
        return render(request, 'homepages/AboutUS.html', args)


def about_us(request):
    """home landing page"""
    return render(request, 'homepages/AboutUs.html')  # 

def create_url(request):
    """URL Create page"""
    return render(request, 'homepages/index.html')  # 

def signout(request):
    """signout view"""
    logout(request)
    messages.success(request, "Logged Out Successfully!")
    return redirect("home")

def delete_all_urls(request):
    """delete all urls"""
    if request.method == "POST":
        username = request.session.get('username')
        if username:
             # Delete URLs for the logged-in user 
            Link.objects.filter(username=username).delete() # pylint: disable=no-member
    return redirect('list')  # Redirect back to the list page
