from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)

  first_name = models.CharField(max_length=20)
  last_name = models.CharField(max_length=20)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class Department(models.Model):
  department_name = models.CharField(max_length=50)
  specialisation = models.CharField(max_length=300)
  departmemt_leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

  def __str__(self):
    return self.department_name

class Team(models.Model):
  
  STATUS_CHOICES = [
    ('on_track', 'On Track'),
    ('at_risk', 'At Risk'),
    ('blocked', 'Blocked')
  ]

  team_name = models.CharField(max_length=50)
  mission = models.CharField(max_length=200)

  department_name = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)

  team_leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
     
  status = models.CharField(max_length=20, choices=STATUS_CHOICES)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.team_name


