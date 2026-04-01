from django.contrib import admin
from .models import Ticket, Agent, KBArticle

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ["subject", "requester_email", "priority", "status", "category", "created_at"]
    list_filter = ["priority", "status"]
    search_fields = ["subject", "requester_email", "category"]

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "department", "role", "tickets_resolved", "created_at"]
    list_filter = ["role"]
    search_fields = ["name", "email", "department"]

@admin.register(KBArticle)
class KBArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "views", "helpful_votes", "status", "created_at"]
    list_filter = ["status"]
    search_fields = ["title", "category"]
