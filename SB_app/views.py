from lib.national_id import NationalID
from django.shortcuts import render , redirect , HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_protect
from .models import *
from datetime import *
from django.core.mail import send_mail
from django.conf import settings
import random
from SB_app import urls
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
config = {
    "apiKey": "AIzaSyDgqQ6j8ETLMvy_cjLsh-crdJ7tN8_ldUo",
    "authDomain": "sbank-30589.firebaseapp.com",
    "databaseURL": "https://sbank-30589-default-rtdb.firebaseio.com",
    "projectId": "sbank-30589",
    "storageBucket": "sbank-30589.appspot.com",
    "messagingSenderId": "1027932140513",
    "appId": "1:1027932140513:web:7125d70d5b3006c0a718a0",
    "measurementId": "G-G2YLVY6Z9N"
}
def custom_page_not_found_view(request, exception):
    return render(request, "404.html", {}, status=404)
def index(request):
    return render(request , 'index.html')
@csrf_protect
def signUp(request):
    if request.method=='POST':
        nationalID = NationalID(request.POST.get('nationalId'))
        if nationalID._validate():
          name = request.POST.get('Name')
          email = request.POST.get('email')
          phone = request.POST.get('phone')
          image = request.FILES.get('userImage')
          password = request.POST.get('password')
          nationalI = request.POST.get('nationalId')
          # send email
          code = random.randint(5000,10000)
          request.session['governorate'] = nationalID.governorate
          request.session['name'] = name
          request.session['email'] = email
          request.session['code'] = code
          request.session['phone'] = phone
          request.session['password'] = password
          request.session['nationalId'] = nationalI
          fs = FileSystemStorage()
          filename = fs.save(image.name, image)
          uploaded_file_url = fs.url(filename)
          request.session['image_url'] = uploaded_file_url
          send_mail("verification code for SBank" , f'Your code is {code}' , settings.EMAIL_HOST_USER , [email], fail_silently=False)
          return redirect(confirmEmail)
        else:
            return render(request , 'signUp.html' , {'validNationalId':"false"})
    return render(request , 'signUp.html')
@csrf_protect
def confirmEmail(request):
    email = request.session.get('email')
    if request.method=="POST":
        name = request.session.get('name')
        phone = request.session.get('phone')
        image = request.session.get('image_url')
        password = request.session.get('password')
        nationalI = request.session.get('nationalId')
        code = request.session.get('code')
        governorate = request.session.get('governorate')
        codeUser = request.POST.get('codeuser')
        if int(code) == int(codeUser):
            newUser = User(name = name , email = email , phone = phone , national_id = nationalI , password = password , balance = 0.00 , image = image , governorate = governorate)
            newUser.save()
            return redirect(home)
        else:
            return render(request, 'confirmEmail.html' , {'check':"false"})
    return render(request , 'confirmEmail.html' , {'userEmail' : email})
@csrf_protect
def signIn(request):
    return render(request , 'signIn.html')
@csrf_protect
def withdraw(request):
    return render(request , 'withdrow.html')
@csrf_protect
def transfer(request):
    return render(request , 'transfer.html')
@csrf_protect
def deposite(request):
    return render(request , 'deposite.html')
def home(request):
    return render(request , 'Home.html')