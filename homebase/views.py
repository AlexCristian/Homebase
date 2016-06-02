from django.shortcuts import get_object_or_404, HttpResponse, render
from .models import User, Assignment, Course, Meeting
import hashlib
from django.core.validators import ValidationError
from datetime import datetime
from django.utils.timezone import utc
from dateutil.parser import parse

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
        assignments = Assignment.objects.filter(
            assoc_user=user
        )
        course_cache = list()
        for assignment in assignments:
            course_cache.append(
                assignment.assoc_course
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
            {"user": user,
             "course_cache": course_cache
             }
        )


def dashboard(request):
    try:
        user = User.objects.get(
            email=request.session["uemail"]
        )
        assignments = Assignment.objects.filter(
            assoc_user=user
        )
        date_asn_pairs = list()
        for assignment in assignments:
            date_asn_pairs.append(
                (assignment.due_date.timestamp(),
                 assignment
                 )
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
            {"assignments": date_asn_pairs
             }
        )


def assignment_details(request, assignment_id):
    if request.session.get("uemail") is None:
        return HttpResponse(
            "404 Not found",
            status=404
        )

    try:
        assignment = Assignment.objects.get(
            id=assignment_id
        )
    except (KeyError, Assignment.DoesNotExist):
        return HttpResponse(
            "404 Not found",
            status=404
        )
    else:
        if assignment.parent_id is None:
            parent_id = -1
        else:
            parent_id = assignment.parent_id.id
        return render(
            request,
            "homebase/assignment_details.json",
            {"assignment": assignment,
             "parent_id": parent_id,
             "due_date_epoch": assignment.due_date.timestamp(),
             "create_date_epoch": assignment.create_date.timestamp(),
             }
        )


def assignment_delete(request, assignment_id):
    if request.session.get("uemail") is None:
        return HttpResponse(
            "404 Not found",
            status=404
        )

    try:
        assignment = Assignment.objects.get(
            id=assignment_id
        )
        assignment.delete()
    except (KeyError, Assignment.DoesNotExist):
        return HttpResponse(
            "404 Not found",
            status=404
        )
    else:
        return HttpResponse(
            "200 Deleted",
            status=200
        )


def get_datetime(string):
    try:
        date = parse(string)
    except (ValueError, OverflowError):
        date = datetime.fromtimestamp(int(string), tz=utc)
    return date


def assignment_new(request):
    try:
        user = User.objects.get(
            email=request.session["uemail"]
        )
        course = Course.objects.get(
            id=request.POST["course_id"]
        )

        if request.POST["parent_id"] == "-1":
            parent = None
        else:
            parent = Assignment.objects.get(
                id=request.POST["parent_id"]
            )

        Assignment.objects.create(
            title=request.POST["title"],
            description=request.POST["description"],
            due_date=get_datetime(request.POST["due_date"]),
            create_date=get_datetime(request.POST["created_at"]),
            type=request.POST["type"],
            assoc_course=course,
            assoc_user=user,
            parent_id=parent
        )
    except (ValidationError, ValueError):
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
    if request.session.get("uemail") is None:
        return HttpResponse(
            "404 Not found",
            status=404
        )

    try:
        course = Course.objects.get(
            id=course_id
        )
    except (KeyError, Course.DoesNotExist):
        return HttpResponse(
            "404 Not found",
            status=404
        )
    else:
        return render(
            request,
            "homebase/course_details.json",
            {"course": course}
        )

        # TODO: implement course serializer


def course_new(request):
    try:
        Course.objects.create(
            title=request.POST["title"],
            section=request.POST["section"]
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
            "200 Course added",
            status=200
        )


def list_meetings(request, course_id):
    if request.session.get("uemail") is None:
        return HttpResponse(
            "404 Not found",
            status=404
        )

    try:
        course = Course.objects.get(
            id=course_id
        )
        meetings = Meeting.objects.filter(
            assoc_course=course
        )
        date_meet_pairs = list()
        for meeting in meetings:
            date_meet_pairs.append(
                (meeting.start_time.timestamp(),
                 meeting.end_time.timestamp(),
                 meeting
                 )
            )
    except (KeyError, Course.DoesNotExist):
        return HttpResponse(
            "404 Not found",
            status=404
        )
    else:
        return render(
            request,
            "homebase/list_meetings.json",
            {"meetings": date_meet_pairs}
        )

        # TODO: implement course serializer


def meeting_new(request):
    if request.session.get("uemail") is None:
        return HttpResponse(
            "404 Not found",
            status=404
        )

    try:
        course = Course.objects.get(
            id=request.POST["course_id"]
        )
        Meeting.objects.create(
            assoc_course=course,
            start_time=get_datetime(request.POST["start_time"]),
            end_time=get_datetime(request.POST["end_time"]),
            location=request.POST["location"],
            recurs=request.POST["recurrence"]
        )
    except (ValidationError, ValueError):
        return HttpResponse(
            "400 Invalid data",
            status=400
        )
    except (KeyError, Meeting.DoesNotExist):
        return HttpResponse(
            "404 Not found",
            status=404
        )
    else:
        return HttpResponse(
            "200 Meeting added",
            status=200
        )


def meeting_delete(request, meeting_id):
    if request.session.get("uemail") is None:
        return HttpResponse(
            "404 Not found",
            status=404
        )

    try:
        meeting = Meeting.objects.get(
            id=meeting_id
        )
        meeting.delete()
    except (KeyError, Meeting.DoesNotExist):
        return HttpResponse(
            "404 Not found",
            status=404
        )
    else:
        return HttpResponse(
            "200 Deleted",
            status=200
        )


def assignment_setparent(request, assignment_id):
    if request.session.get("uemail") is None:
        return HttpResponse(
            "404 Not found",
            status=404
        )

    try:
        assignment = Assignment.objects.get(
            id=assignment_id
        )
        parent = Assignment.objects.get(
            id=request.POST["parent_id"]
        )
        assignment.parent_id = parent
        assignment.save()
    except (KeyError, Assignment.DoesNotExist):
        return HttpResponse(
            "404 Not found",
            status=404
        )
    else:
        return HttpResponse(
            "200 Parent set",
            status=200
        )


def assignment_subtasks(request, assignment_id):
    if request.session.get("uemail") is None:
        return HttpResponse(
            "404 Not found",
            status=404
        )

    try:
        assignment = Assignment.objects.get(
            id=assignment_id
        )
        subtasks = Assignment.objects.filter(
            parent_id=assignment
        )
        date_subt_pairs = list()
        for subtask in subtasks:
            date_subt_pairs.append(
                (subtask.due_date.timestamp(),
                 subtask.create_date.timestamp(),
                 subtask
                 )
            )
    except (KeyError, Assignment.DoesNotExist):
        return HttpResponse(
            "404 Not found",
            status=404
        )
    else:
        return render(
            request,
            "homebase/subtasks.json",
            {"subtasks": date_subt_pairs
             }
        )
