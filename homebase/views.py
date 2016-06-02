from django.shortcuts import get_object_or_404, HttpResponse, render
from .models import User, Assignment
import hashlib
from django.core.validators import ValidationError

# Create your views here.


def signin(request):
    user = get_object_or_404(
        User,
        email=request.POST["email"]
    )
    pwd_hash = hashlib.sha1(
        request.POST["password"].encode('utf-8')
    ).hexdigest()

    if pwd_hash != user.password_sha1:
        return HttpResponse(
            "401 Unauthorized",
            status=401
        )
    else:
        request.session["uemail"] = user.email
        return HttpResponse(
            "200 Login acknowledged",
            status=200
        )


def register(request):
    try:
        User.objects.create(
            name=request.POST["name"],
            email=request.POST["email"],
            password_sha1=hashlib.sha1(
                request.POST["password"].encode('utf-8')
            ).hexdigest(),
            pic_url=request.POST["pic_url"]
        )
    except ValidationError:
        return HttpResponse(
            "400 Invalid registration data",
            status=400
        )
    else:
        return HttpResponse(
            "200 Registration acknowledged",
            status=200
        )


def userdata(request):
    try:
        user = User.objects.get(
            email=request.session["uemail"]
        )
    except KeyError:
        return HttpResponse(
            "404 Not found",
            status=404
        )
    else:
        return render(
            request,
            "homebase/userdata.json",
            {"user": user}
        )

    # TODO: implement userdata serializer
    # raise Http400("Unimplemented function; sorry.")


def dashboard(request):
    try:
        user = User.objects.get(
            email=request.session["uemail"]
        )
    except KeyError:
        return HttpResponse(
            "404 Not found",
            status=404
        )
    else:
        return render(
            request,
            "homebase/dashboard.json",
            {"user": user}
        )
        # TODO: implement userdata serializer
        # raise Http400("Unimplemented function; sorry.")


def assignment_details(request, assignment_id):
    if "uemail" in request.session:
        return HttpResponse(
            "404 Not found",
            status=404
        )

    try:
        assignment = Assignment.objects.get(
            id=assignment_id
        )
    except KeyError:
        return HttpResponse(
            "404 Not found",
            status=404
        )
    else:
        return render(
            request,
            "homebase/assignment_details.json",
            {"assignment": assignment}
        )

        # TODO: implement assignment serializer


def assignment_delete(request, assignment_id):
    if "uemail" in request.session:
        return HttpResponse(
            "404 Not found",
            status=404
        )

    try:
        assignment = Assignment.objects.get(
            id=assignment_id
        )
        assignment.delete()
    except KeyError:
        return HttpResponse(
            "404 Not found",
            status=404
        )
    else:
        return HttpResponse(
            "200 Deleted",
            status=200
        )


def assignment_new(request):
    try:
        Assignment.objects.create(
            title=request.POST["title"],
            description=request.POST["description"],
            due_date=request.POST["due_date"],
            create_date=request.POST["created_at"],
            type=request.POST["type"],
            assoc_course=request.POST["course_id"],
            assoc_user=request.session["uemail"]
        )
    except ValidationError:
        return HttpResponse(
            "400 Invalid data",
            status=400
        )
    except KeyError:
        return HttpResponse(
            "404 Not found",
            status=404
        )
    else:
        return HttpResponse(
            "200 Assignment added",
            status=200
        )


def course_details(request, course_id):
    return HttpResponse(
        "404 Not found",
        status=404
    )


def course_new(request):
    return HttpResponse(
        "404 Not found",
        status=404
    )


def list_meetings(request):
    return HttpResponse(
        "404 Not found",
        status=404
    )


def meeting_new(request):
    return HttpResponse(
        "404 Not found",
        status=404
    )


def meeting_delete(request):
    return HttpResponse(
        "404 Not found",
        status=404
    )
