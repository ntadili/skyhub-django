from django.db import models
from django.contrib.auth.models import User


# ------------------------------------------------
# MODELS CREATED BY NASSER

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)

  first_name = models.CharField(max_length=20)
  last_name = models.CharField(max_length=20)

  team = models.ForeignKey(
    'Team',
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='members'
  )
  department = models.ForeignKey(
    'Department',
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='members'
  )

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"{self.first_name} {self.last_name}"
  

class Department(models.Model):
  department_name = models.CharField(max_length=50)
  specialisation = models.CharField(max_length=300)
  department_leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

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

  @property
  def leader_name(self):
    """Display name of the team leader, preferring their Profile over the raw User."""
    if not self.team_leader:
      return None
    try:
      p = self.team_leader.profile
      return f"{p.first_name} {p.last_name}"
    except Profile.DoesNotExist:
      return self.team_leader.username
  


class Meeting(models.Model):
    FREQUENCY_CHOICES = [
        ('once', 'Once'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]

    title = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    url_link = models.URLField(blank=True, null=True)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='once')

    organiser = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        related_name='organised_meetings'
    )

    participants = models.ManyToManyField(
        Profile,
        related_name='meetings'
    )

    def __str__(self):
        return self.title

# ------------------------------------------------


