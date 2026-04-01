from django.db import models

class Ticket(models.Model):
    subject = models.CharField(max_length=255)
    requester_email = models.EmailField(blank=True, default="")
    priority = models.CharField(max_length=50, choices=[("low", "Low"), ("medium", "Medium"), ("high", "High"), ("critical", "Critical")], default="low")
    status = models.CharField(max_length=50, choices=[("open", "Open"), ("in_progress", "In Progress"), ("waiting", "Waiting"), ("resolved", "Resolved"), ("closed", "Closed")], default="open")
    category = models.CharField(max_length=255, blank=True, default="")
    assigned_to = models.CharField(max_length=255, blank=True, default="")
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.subject

class Agent(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, default="")
    department = models.CharField(max_length=255, blank=True, default="")
    role = models.CharField(max_length=50, choices=[("agent", "Agent"), ("supervisor", "Supervisor"), ("admin", "Admin")], default="agent")
    tickets_resolved = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class KBArticle(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255, blank=True, default="")
    content = models.TextField(blank=True, default="")
    views = models.IntegerField(default=0)
    helpful_votes = models.IntegerField(default=0)
    status = models.CharField(max_length=50, choices=[("draft", "Draft"), ("published", "Published"), ("archived", "Archived")], default="draft")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
