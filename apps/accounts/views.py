from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


from django.views.generic import FormView, CreateView, TemplateView
from django.http import HttpResponse

# Create your views here.

from apps.accounts.forms import LoginForm, UserRegisterForm
from apps.accounts.models import User
from apps.accounts.utils import send_activation_email

class LoginView(FormView):
    template_name="login.html"
    form_class = LoginForm

    def form_valid(self, form):
        data = form.cleaned_data
        email = data["email"]
        password = data["password"]
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return redirect("all")
            else:
                HttpResponse("Ваш аккаунт не активен")
        HttpResponse("Такого пользователя не существует или данные неверны")

    
# В каждом из request переменных хранится user.
# Если запрос отправлен авторизованным пользователем, то там хранится данные сущ.
# пользователя
# В случае если запрос отправлен без авторизации , то request.user хранит анонимного 
# пользователя.

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("all")


from django.urls import reverse_lazy

class UserRegisterView(CreateView):
    model = User
    template_name = "register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("register_done")

    def form_valid(self, form):
        user = form.save()
        send_activation_email(user,request=self.request, to_email=user.email)
        return super().form_valid(form)



class RegisterDoneView(TemplateView):
    template_name = "register_done.html"



from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.http import Http404

from apps.accounts.token import CustomTokenGenerator

token_generator = CustomTokenGenerator()

def activate_account(request,uidb64, token):
    try:
        uid = int(force_str(urlsafe_base64_decode(uidb64)))
        user = User.objects.get(id=uid)
    except (ValueError, User.DoesNotExist, TypeError):
        user = None
    if user is not None and token_generator.check_token(user, token):
        user.is_verified = True
        login(request, user)
        return redirect(reverse_lazy('all'))
    raise Http404