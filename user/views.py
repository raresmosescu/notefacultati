from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.conf import settings
from django.urls import reverse
from django.core.mail import send_mail
import random, string
from .models import AuthUser



# Create your views here.
def user_create(request):
	if request.POST:
		pw = request.POST.get('password')
		email = request.POST.get('email')
		if not User.objects.filter(username=email).exists():
			activation_code = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
			user = User.objects.create_user(username = email, email=email, password=pw, is_active=False)
			user = AuthUser.objects.get(id=user.id)
			user.activation_code = activation_code
			user.save()
			messages.success(request, message=f'Email-ul de activare a contului a fost trimis la adresa {email}.')
			# send_mail(
			#     'Verifica-ti contul',
			#     f'Copiaza codul https://www.noteprofesori.ro/user/activate?code={hash_code}',
			#     'no-reply@noteprofesori.ro',
			#     [email],
			#     fail_silently=False,
			# )
			send_mail(
			    'Verifica-ti contul',
			    f'''Da click pe link pentru a verifica contul: \n
			    https://www.noteprofesori.ro/user/activate?id={user.id}&code={user.activation_code}''',
			    'no-reply@noteprofesori.ro',
			    [email],
			    fail_silently=False,
			)
			return redirect('%s?next=%s' % (reverse(settings.LOGIN_URL), request.path))
		else:
			messages.warning(request, message='Email-ul exista deja')
			return redirect('%s?next=%s' % (reverse(settings.LOGIN_URL), request.path))
	return render(request, template_name='user_create.html')


def login_view(request):
	if request.POST:
		email = request.POST['login-email']
		pw = request.POST['login-password']
		user = authenticate(request, username=email, password=pw)
		if user is not None: 
			login(request, user)
			messages.success(request, message='Logare reusita.')
			if request.GET.get('next'):
				return redirect(request.GET.get('next'))
			else:
				return redirect('/')
		else:
			messages.warning(request, message='Email sau parola incorecta. Incearca din nou.')
			return redirect('%s?next=%s' % (reverse(settings.LOGIN_URL), request.GET.get('next')))
	return render(request, template_name='login.html')


def logout_view(request):
    logout(request)
    messages.info(request, message="Ai iesit din cont.")
    return redirect(request.GET.get('next'))
    # Redirect to a success page.


def user_profile(request):
	if not request.user.is_authenticated:
		return redirect('%s?next=%s' % (reverse(settings.LOGIN_URL), request.path))
	if request.POST:
		# change user info
		pw = request.POST.get('password')
		email = request.POST.get('email')
		if pw:
			request.user.set_password(pw)
		request.user.email = email
		request.user.username = email
		request.user.save()
		messages.success(request, message='Datele au fost salvate cu succes.')
		return redirect('user:user_profile')
	else:
		return render(request, template_name="user_profile.html")



def user_activate(request):
	if request.GET:
		code = request.GET.get('code')
		user_id = request.GET.get('id')
		user = AuthUser.objects.get(id=user_id)
		print(code, user.activation_code)
		if user.activation_code == code:
			user.is_active = 1
			user.save()
			messages.success(request, message="Contul tau a fost activat.")
			return redirect('%s?next=%s' % (reverse(settings.LOGIN_URL), '/'))
		else:
			messages.warning(request, message="Codul de activare e incorect.")
			return redirect('/')
	else:
		messages.warning(request, message="E o problema cu activarea contului tau. Daca persista, contacteaza-ne.")
		return redirect('/')
	redirect('/')