from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, CreateView
from django.contrib.auth import get_user_model
from info.forms import CustomUserCreationForm
from info.models import Student

User = get_user_model()
# Create your views here.

@login_required
def index(request):
    if request.user.is_teacher:
        return render(request, 'info/t_homepage.html')
    if request.user.is_student:
        return render(request, 'info/s_homepage.html')
    return render(request, 'registration/login.html')

class LandingPageView(TemplateView):
    template_name = "landing.html"