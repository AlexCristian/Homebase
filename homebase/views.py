from django.shortcuts import get_object_or_404, HttpResponse, render
from .models import User
import hashlib
from django.core.validators import ValidationError

# Create your views here.


def signin(request):
    user = get_object_or_404(
        User,
        username=request["username"]
    )
    pwd_hash = hashlib.sha1(
        request["password"]
    ).digest()

    if pwd_hash != user.password_sha1:
        return HttpResponse("401 unauthorized", code=401)
    else:
        request.session["uemail"] = user.email
        return HttpResponse(
            "200 Login acknowledged",
            code=200
        )


def register(request):
    try:
        User.objects.create(
            name=request["name"],
            email=request["email"],
            password_sha1=hashlib.sha1(
                request["password"]
            ).digest(),
            pic_url=request["pic_url"]
        )
    except ValidationError:
        return HttpResponse(
            "400 Invalid registration data",
            code=400
        )
    else:
        return HttpResponse(
            "200 Registration acknowledged",
            code=200
        )


def get_session_user(request):
    return get_object_or_404(
        User,
        email=request.session["uemail"]
    )


def userdata(request, user_id):
    user = get_session_user(request)

    return render(
        request,
        "homebase/userdata.json",
        {"user": user}
    )

    # TODO: implement userdata serializer
    # raise Http400("Unimplemented function; sorry.")


def dashboard(request):
    user = get_session_user(request)

    return render(
        request,
        "homebase/dashboard.html",
        {"user": user}
    )
    # TODO: implement userdata serializer
    # raise Http400("Unimplemented function; sorry.")
