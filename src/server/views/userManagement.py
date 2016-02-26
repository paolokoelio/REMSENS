from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from server.forms import UserForm, UserProfileForm

BASE_URL = 'remsens'

###### AUTHENTICATION STUFF #######

def register(request):

    registered = False

    if request.method == 'POST':
        
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            # password hashing
            user.set_password(user.password)
            user.is_active = False
            user.save()

            # resolves integrity problems
            profile = profile_form.save(commit=False)
            profile.user = user

            # save the UserProfile model instance.
            profile.save()

            # registration successful
            registered = True

        # Print problems to the terminal.
        else:           
            print (user_form.errors, profile_form.errors)

    # Non un HTTP POST, cioe la pagina di registrazione e' stata aperta
    # Form vuoti:
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # renderizzo il template per i miei scopi.
    return render(request,
            BASE_URL + '/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})
    
def user_login(request):

    if request.method == 'POST':
        # Gather the username and password provided by the user.
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct,
        # if no, no user with matching credentials was found
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print ("Invalid login details: {0}, {1}").format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, BASE_URL + '/login.html', {})

@login_required
def user_logout(request):
    logout(request)
    # take the user back to the homepage.
    return HttpResponseRedirect('/')
        