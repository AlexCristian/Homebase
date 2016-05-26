from django.shortcuts import get_object_or_404, HttpResponse, render, Http400
from .models import User
import hashlib

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
        request.session["uid"] = user.id
        return HttpResponse(
            "200 Login acknowledged",
            code=200
        )


def get_session_user(request):
    return get_object_or_404(
        User,
        id=request.session["uid"]
    )


def userdata(request):
    user = get_session_user(request)
    '''
    return render(
        request,
        "homebase/userdata.json",
        {"user": user}
    )
    '''
    # TODO: implement userdata serializer
    raise Http400("Unimplemented function; sorry.")


def dashboard(request):
    user = get_session_user(request)

    # TODO: implement userdata serializer
    raise Http400("Unimplemented function; sorry.")
