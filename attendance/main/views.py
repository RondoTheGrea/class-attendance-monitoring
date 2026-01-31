from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group

from .forms import StudentSignUpForm, ProfessorSignUpForm


from django.contrib import messages

def home(request):
    context = {}
    if request.method == "POST":
        if 'student_login' in request.POST:
            student_login_form = AuthenticationForm(request, data=request.POST)
            if student_login_form.is_valid():
                user = student_login_form.get_user()
                if not user.groups.filter(name="student").exists():
                    student_login_form.add_error(None, "This account is not registered as a student.")
                else:
                    login(request, user)
                    return redirect("student:dashboard")
            context['student_login_form'] = student_login_form
            context['professor_login_form'] = AuthenticationForm()
        elif 'professor_login' in request.POST:
            professor_login_form = AuthenticationForm(request, data=request.POST)
            if professor_login_form.is_valid():
                user = professor_login_form.get_user()
                if not user.groups.filter(name="professor").exists():
                    professor_login_form.add_error(None, "This account is not registered as a professor.")
                else:
                    login(request, user)
                    return redirect("professor:dashboard")
            context['professor_login_form'] = professor_login_form
            context['student_login_form'] = AuthenticationForm()
        else:
            context['student_login_form'] = AuthenticationForm()
            context['professor_login_form'] = AuthenticationForm()
    else:
        context['student_login_form'] = AuthenticationForm()
        context['professor_login_form'] = AuthenticationForm()
    return render(request, "main/home.html", context)


def _get_or_create_group(name: str) -> Group:
    group, _ = Group.objects.get_or_create(name=name)
    return group


def student_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.groups.filter(name="student").exists():
                form.add_error(None, "This account is not registered as a student.")
            else:
                login(request, user)
                return redirect("student:dashboard")
    else:
        form = AuthenticationForm(request)

    return render(request, "main/student_login.html", {"form": form})


def student_signup(request):
    if request.method == "POST":
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            student_group = _get_or_create_group("student")
            user.groups.add(student_group)
            login(request, user)
            return redirect("student:dashboard")
    else:
        form = StudentSignUpForm()

    return render(request, "main/student_signup.html", {"form": form})


def professor_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.groups.filter(name="professor").exists():
                form.add_error(None, "This account is not registered as a professor.")
            else:
                login(request, user)
                return redirect("professor:dashboard")
    else:
        form = AuthenticationForm(request)

    return render(request, "main/professor_login.html", {"form": form})


def professor_signup(request):
    if request.method == "POST":
        form = ProfessorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            prof_group = _get_or_create_group("professor")
            user.groups.add(prof_group)
            login(request, user)
            return redirect("professor:dashboard")
    else:
        form = ProfessorSignUpForm()

    return render(request, "main/professor_signup.html", {"form": form})
