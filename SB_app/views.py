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
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
import base64
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.shortcuts import get_object_or_404
from django.db.models import Q
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
        nationalI = request.POST.get('nationalId')
        checkForN = User.objects.filter(national_id = nationalI).first()
        if checkForN is None:  
            nationalID = NationalID(request.POST.get('nationalId'))
            if nationalID._validate():
                name = request.POST.get('Name')
                email = request.POST.get('email')
                phone = request.POST.get('phone')
                image = request.FILES.get('userImage')
                password = request.POST.get('password')
                
                # send email
                code = random.randint(5000,10000)
                request.session['governorate'] = nationalID.governorate
                request.session['name'] = name
                request.session['email'] = email
                request.session['code'] = code
                request.session['phone'] = phone
                request.session['password'] = password
                request.session['nationalId'] = nationalI
                if image:
                        image_data = image.read()
                        encoded_image = base64.b64encode(image_data).decode('utf-8')
                        request.session['image'] = encoded_image
                        request.session['image_name'] = image.name
                send_mail("verification code for SBank" , f'Your code is {code}' , settings.EMAIL_HOST_USER , [email], fail_silently=False)
                return redirect(confirmEmail)
            else:
                return render(request , 'signUp.html' , {'validNationalId':"false"})
        else:
             return render(request , 'signUp.html' , {'hastooken':"false"})
    return render(request , 'signUp.html')
@csrf_protect
@login_required(login_url='signUp')
def confirmEmail(request):
    email = request.session.get('email')
    if request.method=="POST":
        name = request.session.get('name')
        phone = request.session.get('phone')
        password = request.session.get('password')
        nationalI = request.session.get('nationalId')
        code = request.session.get('code')
        governorate = request.session.get('governorate')
        codeUser = request.POST.get('codeuser')
        encoded_image = request.session.get('image')
        image_name = request.session.get('image_name')
        date_of_creation = datetime.now().strftime("%Y-%m-%d")
        if encoded_image and image_name:
                image_data = base64.b64decode(encoded_image)
                image_file = ContentFile(image_data, name=image_name)
                image_path = default_storage.save(f'user_images/{image_name}', image_file)
        else:
                image_path = None
        if int(code) == int(codeUser):
            newUser = User(name = name , email = email , phone = phone , national_id = nationalI , password = password , balance = 0.00 , image=image_path , governorate = governorate , date_of_creation=date_of_creation)
            newUser.save()
            return redirect(home)
        else:
            return render(request, 'confirmEmail.html' , {'check':"false"})
    return render(request , 'confirmEmail.html' , {'userEmail' : email , 'check':"true"})
@csrf_protect
def signIn(request):
    if request.method == 'POST':
        nationalIDuser = request.POST.get('nationalIDfromuser')
        password = request.POST.get('password')
        if nationalIDuser and password :
            try:
                check = User.objects.get(national_id=nationalIDuser , password = password)
                if check:
                    request.session['nationalId'] = nationalIDuser
                    return redirect(home)
            except ObjectDoesNotExist:
                return render(request, 'signIn.html' , {'check':'false'})
    return render(request, 'signIn.html' , {'check':'true'})
@csrf_protect
@login_required(login_url='signUp')
def withdraw(request):
    national_id = request.session.get('nationalId')
    user = User.objects.filter(national_id = national_id).first()
    if request.method == "POST":
        amount = request.POST.get('amount')
        if user.balance >=float(amount):
            user.balance -= float(amount)
            user.save()
            icon = 'success'
            message = f'Success Process Your Balance is {user.balance}'
            return render(request , 'withdrow.html' , {"icon" : icon , 'user':user , 'message' : message})
        else:
            icon = 'error'
            message = f'Fail process Your balance is not Enough : Your balance is  {user.balance}'
            return render(request , 'withdrow.html' , {"icon" : icon , "message":message , 'user':user})
    return render(request , 'withdrow.html' , {'user':user})
@csrf_protect
@login_required(login_url='signUp')
def transfer(request):
    national_id = request.session.get('nationalId')
    user = get_object_or_404(User, national_id=national_id)
    if request.method == "POST":
        user2_name = request.POST.get('user')
        amount = request.POST.get('amount')
        if user2_name and amount:
            try:
                user2 = User.objects.filter( name = user2_name ).first()
                if(user.balance >= float(amount)):
                    user2.balance += float(amount) 
                    user.balance -= float(amount)
                    new_process = Transfers.objects.create(
                            balance=float(amount),
                            date_of_process = datetime.now().strftime("%Y-%m-%d"),
                            from_user=user,
                            to_user=user2
                        )
                    user.save()
                    user2.save()
                    new_process.save()
                    message = "Success Process Your balance is {} {}".format(user.balance, user.coin[:2])
                    icon = "success"
                    return render(request, 'transfer.html', {'message': message , 'user':user , 'icon' : icon})
                
                else:
                    message = "Your balance is not enough"
                    icon = "error"
                    return render(request, 'transfer.html', {'message': message , 'user':user , 'icon' :icon})
            
            except User.DoesNotExist:
                message = "No user found"
                icon ="error"
                return render(request, 'transfer.html', {'message': message , 'user':user, 'icon' :icon})
        
        else:
            message = "There is an empty field"
            icon="error"
            return render(request, 'transfer.html', {'message': message , 'user':user, 'icon' :icon})
    
    return render(request, 'transfer.html' , {'user':user})
@csrf_protect
@login_required(login_url='signUp')
def deposite(request):
    national_id = request.session.get('nationalId')
    user = get_object_or_404(User, national_id=national_id)
    if request.method == "POST":
        amount = request.POST.get('amount')
        if amount:
            amount = float(amount)
            user.balance+=amount
            user.save()
            message = f"Success! Your balance is {user.balance} {user.coin[:2]}"
            icon = "success"
        else:
            message = "There is an empty field"
            icon = "error"
        return render(request, 'deposite.html', {'message': message , "icon" : icon , "user":user })
    return render(request, 'deposite.html' , {"user":user })
@login_required(login_url='signUp')
def home(request):
    nationalId = request.session.get('nationalId')
    user = User.objects.get(national_id = nationalId)
    transfers = Transfers.objects.filter(Q(from_user=user) | Q(to_user=user))
    return render(request , 'Home.html' , {'user' : user  , 'transfers':transfers})
@login_required(login_url='signUp')
def profile(request):
    nationalId = request.session.get('nationalId')
    user = User.objects.get(national_id=nationalId)
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        email = request.POST.get('email')
        user.phone = phone
        user.mobile = phone
        user.email = email
        user.password = password
        user.name = name
        user.balance = user.balance
        user.governorate = user.governorate
        user.national_id = user.national_id
        user.date_of_creation = user.date_of_creation
        user.save()
        return render(request, 'profile.html', {'user': user , 'CheckUpdate':"true"})
    return render(request, 'profile.html', {'user': user})

