from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/Student/', null=True, blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=False)
    tenth_marks = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    twelfth_marks = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    graduation_marks = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    BRANCH_CHOICES = [
        ('CS', 'Computer Science'),
        ('CE', 'Circuit'),
        ('ME', 'Mechanical'),
        ('CH', 'Chemical'),
    ]
    graduation_branch = models.CharField(max_length=2, choices=BRANCH_CHOICES)
    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_instance(self):
        return self

    def __str__(self):
        return self.user.first_name
    
    def __str__(self):
      return self.user

class EligibleCompany(models.Model):
    name = models.CharField(max_length=100)
    minimum_10th_marks = models.DecimalField(max_digits=5, decimal_places=2)
    minimum_12th_marks = models.DecimalField(max_digits=5, decimal_places=2)


    
