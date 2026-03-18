from typing import Any

from django.db import models
from django.contrib.auth.models import AbstractUser
# from apps.contracts.models import Contract
# from apps.users.models import User
# from apps.projects.models import Project



class User(AbstractUser):

    ROLE_CHOICES = (
        ('client', 'client'),
        ('freelancer', 'freelancer'),
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email



class Review(models.Model):
    RATING_CHOICES = [(i, i) for i in range(1, 6)]

    contract = models.OneToOneField('Contract', on_delete=models.CASCADE, related_name='review')
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.contract.project.title} by {self.contract.client.username}"



class Project(models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    title = models.CharField(max_length=255)
    description = models.TextField()
    budget = models.DecimalField(max_digits=12, decimal_places=2)
    deadline = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f"{self.title} - {self.client.username}"



class Contract(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('finished', 'Finished'),
        ('cancelled', 'Cancelled'),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='contracts')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contracts_as_client')
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contracts_as_freelancer')
    agreed_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.project.title} - {self.client.username} & {self.freelancer.username}"



class Bid(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="bids")
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    price = models.DecimalField(max_digits=12, decimal_places=2)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        pass
        #     unique_together = ('project', 'freelancer')


    def __str__(self):
        return f"{self.project.title} - {self.freelancer.username} - {self.price}"

class ChatMessage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="messages")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"{self.user.username}: {self.text[:20]}"

