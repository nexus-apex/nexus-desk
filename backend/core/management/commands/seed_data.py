from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Ticket, Agent, KBArticle
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seed NexusDesk with demo data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@nexusdesk.com', 'Admin@2024')
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        if Ticket.objects.count() == 0:
            for i in range(10):
                Ticket.objects.create(
                    subject=f"Sample Ticket {i+1}",
                    requester_email=f"demo{i+1}@example.com",
                    priority=random.choice(["low", "medium", "high", "critical"]),
                    status=random.choice(["open", "in_progress", "waiting", "resolved", "closed"]),
                    category=f"Sample {i+1}",
                    assigned_to=f"Sample {i+1}",
                    description=f"Sample description for record {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 Ticket records created'))

        if Agent.objects.count() == 0:
            for i in range(10):
                Agent.objects.create(
                    name=["Rajesh Kumar","Priya Sharma","Amit Patel","Deepa Nair","Vikram Singh","Ananya Reddy","Suresh Iyer","Meera Joshi","Karthik Rao","Fatima Khan"][i],
                    email=f"demo{i+1}@example.com",
                    department=f"Sample {i+1}",
                    role=random.choice(["agent", "supervisor", "admin"]),
                    tickets_resolved=random.randint(1, 100),
                    rating=round(random.uniform(1000, 50000), 2),
                    active=random.choice([True, False]),
                )
            self.stdout.write(self.style.SUCCESS('10 Agent records created'))

        if KBArticle.objects.count() == 0:
            for i in range(10):
                KBArticle.objects.create(
                    title=f"Sample KBArticle {i+1}",
                    category=f"Sample {i+1}",
                    content=f"Sample content for record {i+1}",
                    views=random.randint(1, 100),
                    helpful_votes=random.randint(1, 100),
                    status=random.choice(["draft", "published", "archived"]),
                )
            self.stdout.write(self.style.SUCCESS('10 KBArticle records created'))
