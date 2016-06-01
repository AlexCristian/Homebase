from django.db import models
from django.core.validators import EmailValidator
from django.db.models.signals import pre_save
from django.dispatch import receiver


# Create your models here.


@receiver(pre_save)
def pre_save_handler(sender, instance, *args, **kwargs):
    instance.full_clean()


class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200,
                              primary_key=True,
                              unique=True,
                              validators=[EmailValidator])

    # SHA1 always 160 bits long = 20 bytes
    password_sha1 = models.BinaryField(max_length=20)

    pic_url = models.URLField()


class Course(models.Model):
    title = models.CharField(max_length=200)
    section = models.CharField(max_length=20)


class Assignment(models.Model):
    assoc_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    create_date = models.DateTimeField(auto_now=True)

    PAPER = "PP"
    DISCUSSION_POST = "DP"
    GROUP_PROJECT = "GP"
    LAB = "LB"
    ASSIGNMENT_TYPE_CHOICES = {
        (PAPER, "Paper"),
        (DISCUSSION_POST, "Discussion post"),
        (GROUP_PROJECT, "Group project"),
        (LAB, "Lab")
    }
    type = models.CharField(
        max_length=2,
        choices=ASSIGNMENT_TYPE_CHOICES)

    assoc_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )


class Meeting(models.Model):
    assoc_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=200)

    WEEKLY = "W"
    BI_WEEKLY = "B"
    MONTHLY = "M"
    MEETING_RECURRENCE_CHOICES = {
        (WEEKLY, "Weekly"),
        (BI_WEEKLY, "Bi-weekly"),
        (MONTHLY, "Monthly")
    }
    recurs = models.CharField(
        max_length=1,
        choices=MEETING_RECURRENCE_CHOICES
    )
