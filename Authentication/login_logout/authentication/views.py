from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from authentication.models import TodoList


# Create your views here.


def login_(request):
    if request.user.is_authenticated:
        return redirect("/home/")

    if request.method == "POST":
        data = request.POST

        username = data.get("username")
        password = data.get("password")

        user_name = User.objects.filter(username=username).exists()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/home/")
        else:
            messages.warning(request, "Invalid Usernmame and Password")

    return render(request, "index.html")


@login_required
def home(request):
    user = request.user
    # print(user, "-----------------------")
    all_todo = TodoList.objects.filter(user=user)
    # print(all_todo)

    if request.method == "POST":
        try:
            data = request.POST

            title = data.get("todo_tittle")

            todo = TodoList.objects.create(user=user, title=title)

            # print(todo)
            return redirect("/home/")
        except Exception as e:
            print(e)
    return render(
        request, "home.html", context={"website": "Home", "all_todo": all_todo}
    )


def register(request):
    if request.user.is_authenticated:
        return redirect("/home/")

    if request.method == "POST":
        data = request.POST

        name = data.get("first_name")
        username = data.get("username")
        password = data.get("password")

        # print(f"{name}, {username}, {password}")

        if User.objects.filter(username=username).exists():
            messages.warning(request, "User Already Register")

        else:
            user = User.objects.create_user(
                username=username, password=password, first_name=name
            )
            messages.success(request, "Account Created Succesfully")

        #     return redirect("/register/")

    return render(request, "register.html")


def logout_(request):
    logout(request)
    return redirect("/")


@login_required
def delete(request, id):
    delete_todo = TodoList.objects.filter(id=id).delete()
    return redirect("/home/")
