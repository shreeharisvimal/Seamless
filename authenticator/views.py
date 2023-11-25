
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.views.decorators.cache import cache_control
from django.contrib import messages
from user_side.models import NewUser
import random
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

OTP_EXPIRATION_SECONDS = 120

def email_send(email,otp):

    send_mail(
        'Seamless OTP Verification Code',
        f'''Dear {email},

        We hope this message finds you well. At Seamless, your security and convenience are our top priorities. We're excited to help you complete your verification process, and we're just one step away.

        To verify your account, please use the following OTP (One-Time Password):

        Your OTP: {otp}

        Please note that this OTP is only valid for a single use and will expire shortly, so act swiftly.

        If you didn't initiate this verification, please contact our support team immediately.

        Thank you for choosing Seamless. We're here to make your experience as smooth as possible. If you have any questions or need assistance, don't hesitate to reach out to our support team at yourseamlesslife@gmail.com.

        Best regards,
        The Seamless Team
        ''',
        'yourseamlesslife@gmail.com',
        [email],
        fail_silently=False,
    )

@cache_control(no_cache=True, must_revalidate=True, max_age=0,no_store = True)
def otp_verify(request):
    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        if entered_otp == request.session.get('otp_key'):
            user = authenticate(request, email=request.session.get('email'), password=request.session.get('password'))
            if user is not None:
                login(request, user)
                return redirect('user_side:landing')
            if user is None:
                NewUser.new_manager.create_user(
                    username = request.session['username'],
                    email = request.session['email'],
                    phone_number =  request.session['phone'], 
                    password = request.session['password'], 
                )
                user = authenticate(request, email=request.session.get('email'), password=request.session.get('password'))
                login(request, user)
                return redirect('user_side:landing')            
        elif 'resend' in request.POST:
            login_otp = random.randint(100000, 999999)
            request.session['otp_key'] = str(login_otp)
            email_send(request.session.get('email'), request.session.get('otp_key'))
            messages.info(request, 'OTP resent successfully!')
        elif entered_otp != request.session.get('otp_key'):
            messages.warning(request, 'OTP is wrong !')
        elif entered_otp is None:
            messages.warning(request, 'Enter the OTP !')

    return render(request, 'otp_login.html')



@cache_control(no_cache=True, must_revalidate=True, max_age=0,no_store = True)
def login_handler(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_side:admin_dash_handler')
        return redirect('user_side:landing')

    if request.method == "POST":
        email = request.POST['log_id']
        password = request.POST['password']
        request.session['email'] = email
        request.session['password'] = password
        print(email, password)
        user = authenticate(request, email=email, password=password)
        if user is not None:
            if not user.is_active:
                messages.warning(request, "THE ACCOUNT IS BLOCKED")
                return redirect('authentication:login_handler')
            if user.is_superuser:
                messages.warning(request, " 😓 admin can't login in here")
                return redirect('authentication:login_handler')
            
            login_otp = random.randint(100000, 999999)
            request.session['otp_key'] = str(login_otp)
            email_send(request.session['email'],request.session['otp_key'])
            return redirect('authentication:otp_verify')
                
        else:
            messages.warning(request, " 😓 Invalid username or password")
            return redirect('authentication:login_handler')

    return render(request, 'authentication/login.html')



# @cache_control(no_cache=True, must_revalidate=True, max_age=0,no_store = True)
def sign_handler(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_side:admin_dash_handler')
        return redirect('user_side:landing')
    
    if request.method == "POST":
        username = request.POST["uname"]
        email = request.POST["email"]
        phone = request.POST['phone']
        password1= request.POST["pass1"]
        password2 = request.POST["pass2"]
        request.session['username'] = username
        request.session['email'] = email
        request.session['phone'] = phone
        request.session['password'] = password1

        if not username:
            messages.warning(request, "Enter a username")
            return redirect('authentication:sign_handler')
        try:
            validate_email(email)
        except ValidationError:
            messages.warning(request, "Invalid email or Field is empty")
            return redirect('authentication:sign_handler')
        if not phone:
            messages.warning(request, "Enter Your Phone Number")
            return redirect('authentication:sign_handler')
        if not password1:
            messages.warning(request, "Field for password 1 is not filled")
            return redirect('authentication:sign_handler')
        if not password2:
            messages.warning(request, "Field for password 2 is not filled")
            return redirect('authentication:sign_handler')
        if  len(password1) < 5:
            messages.warning(request, "Minimum characters required for password")
            return redirect('authentication:sign_handler')
        if password1 != password2:
            messages.warning(request, "Oops! The passwords don't match.")
            return redirect('authentication:sign_handler')
        try:
            if NewUser.new_manager.get(Q(email=email)):
                messages.warning(request, "Oops! The email is already in use.")
                return redirect('authentication:sign_handler')
        except NewUser.DoesNotExist:
            pass
             
        try:
           if NewUser.new_manager.get(username=username):
                messages.warning(request, "Oops! The name is already in use.")
                return redirect('authentication:sign_handler')
        except NewUser.DoesNotExist:
            pass
       
        login_otp = random.randint(100000, 999999)
        request.session['otp_key'] = str(login_otp)
        email_send(request.session['email'],request.session['otp_key'])
        return redirect('authentication:otp_verify') 
        
    return render(request, 'authentication/sign.html')



@cache_control(no_cache=True, must_revalidate=True, max_age=0,no_store = True)
def logout_handler(request):
    logout(request)
    messages.info(request,"You have logged out successfully.")
    return redirect('user_side:landing')


