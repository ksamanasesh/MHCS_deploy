from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from .models import user_details,ChatMesage
from .forms import user_details,userForm
from fuzzywuzzy import fuzz
from .services import chat_session,get_special_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai

# Create your views here.

def testing(request):
    text = '<h1>Mental Health Care Support</h1>'
    return HttpResponse(text)

@csrf_exempt  
def signUp(request):
    numbers = ['1','2','3','4','5','6','7','8','9','0']
    numeric = False
    similarity = 55
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        similar = fuzz.ratio(username,pass1)

        if len(pass1) < 8 :
            min_words = "Password must contain atleast 8 characters"
            return render(request,'signUp.html',context={'min_words':min_words})

        else:
            if pass1 == pass2 :
                createUser = User.objects.create_user(first_name=fname,last_name=lname,username=username, email=email, password=pass1)
                createUser.first_name = fname
                createUser.last_name = lname
                createUser.save()
            else :
                noMatch = "Password doesn't match"
                return render(request,'signUp.html',context={'noMatch':noMatch})
            
            success = "Your account has been created Successfully, Login Here"
            print(success)
            return redirect('/signIn')
    return render(request,'signUp.html')

def signIn(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass1']

        user = authenticate(username=username, password=password)
        if user is not None :
            lname = user.last_name
            welcome = f"Hello, {lname}"
            login(request, user)
            return render(request,'home.html',context={'welcome':welcome})
        else :
            error = "Incorrect Username or Password"
            return render(request,'new_home.html',context={'error':error})
    return render(request,'new_home.html')

def home(request):
    return render(request,'home.html')

def signOut(request):
    logout(request)
    logOut = "Successfully logged Out"
    return render(request,'home.html',context={'logOut':logOut})

def user_profile(request):
    if request.method == 'POST':
        form = userForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            return redirect('/user_profile_view')
        else:
            form = user_details
            return render(request,'user_profile.html',{'form':form})
    return render(request,'user_profile.html')

def user_profile_view(request):
    user_detail = user_details.object.all()
    user_info = {'user_details': user_detail}
    return render(request,"user_profile_view.html", user_info)

@csrf_exempt  
def chat_view(request):
    if request.method == 'POST':
            data = json.loads(request.body)
            user_message = data.get('message', '')
            special_response = get_special_response(user_message)
            if special_response:
                return JsonResponse({"response": special_response})
            response = chat_session.send_message(user_message)

            return JsonResponse({"response": response.text})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

def chat_page(request):
    return render(request, 'chat.html')

# @login_required
# def chat_history(request):
#     history = Chat.objects.filter(user=request.user).order_by('timestamp')

#     return render(request, 'chat_history.html', {'history': history})