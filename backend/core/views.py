import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count
from .models import Ticket, Agent, KBArticle


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        error = 'Invalid credentials. Try admin / Admin@2024'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def dashboard_view(request):
    ctx = {}
    ctx['ticket_count'] = Ticket.objects.count()
    ctx['ticket_low'] = Ticket.objects.filter(priority='low').count()
    ctx['ticket_medium'] = Ticket.objects.filter(priority='medium').count()
    ctx['ticket_high'] = Ticket.objects.filter(priority='high').count()
    ctx['agent_count'] = Agent.objects.count()
    ctx['agent_agent'] = Agent.objects.filter(role='agent').count()
    ctx['agent_supervisor'] = Agent.objects.filter(role='supervisor').count()
    ctx['agent_admin'] = Agent.objects.filter(role='admin').count()
    ctx['agent_total_rating'] = Agent.objects.aggregate(t=Sum('rating'))['t'] or 0
    ctx['kbarticle_count'] = KBArticle.objects.count()
    ctx['kbarticle_draft'] = KBArticle.objects.filter(status='draft').count()
    ctx['kbarticle_published'] = KBArticle.objects.filter(status='published').count()
    ctx['kbarticle_archived'] = KBArticle.objects.filter(status='archived').count()
    ctx['recent'] = Ticket.objects.all()[:10]
    return render(request, 'dashboard.html', ctx)


@login_required
def ticket_list(request):
    qs = Ticket.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(subject__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(priority=status_filter)
    return render(request, 'ticket_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def ticket_create(request):
    if request.method == 'POST':
        obj = Ticket()
        obj.subject = request.POST.get('subject', '')
        obj.requester_email = request.POST.get('requester_email', '')
        obj.priority = request.POST.get('priority', '')
        obj.status = request.POST.get('status', '')
        obj.category = request.POST.get('category', '')
        obj.assigned_to = request.POST.get('assigned_to', '')
        obj.description = request.POST.get('description', '')
        obj.save()
        return redirect('/tickets/')
    return render(request, 'ticket_form.html', {'editing': False})


@login_required
def ticket_edit(request, pk):
    obj = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        obj.subject = request.POST.get('subject', '')
        obj.requester_email = request.POST.get('requester_email', '')
        obj.priority = request.POST.get('priority', '')
        obj.status = request.POST.get('status', '')
        obj.category = request.POST.get('category', '')
        obj.assigned_to = request.POST.get('assigned_to', '')
        obj.description = request.POST.get('description', '')
        obj.save()
        return redirect('/tickets/')
    return render(request, 'ticket_form.html', {'record': obj, 'editing': True})


@login_required
def ticket_delete(request, pk):
    obj = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/tickets/')


@login_required
def agent_list(request):
    qs = Agent.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(role=status_filter)
    return render(request, 'agent_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def agent_create(request):
    if request.method == 'POST':
        obj = Agent()
        obj.name = request.POST.get('name', '')
        obj.email = request.POST.get('email', '')
        obj.department = request.POST.get('department', '')
        obj.role = request.POST.get('role', '')
        obj.tickets_resolved = request.POST.get('tickets_resolved') or 0
        obj.rating = request.POST.get('rating') or 0
        obj.active = request.POST.get('active') == 'on'
        obj.save()
        return redirect('/agents/')
    return render(request, 'agent_form.html', {'editing': False})


@login_required
def agent_edit(request, pk):
    obj = get_object_or_404(Agent, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.email = request.POST.get('email', '')
        obj.department = request.POST.get('department', '')
        obj.role = request.POST.get('role', '')
        obj.tickets_resolved = request.POST.get('tickets_resolved') or 0
        obj.rating = request.POST.get('rating') or 0
        obj.active = request.POST.get('active') == 'on'
        obj.save()
        return redirect('/agents/')
    return render(request, 'agent_form.html', {'record': obj, 'editing': True})


@login_required
def agent_delete(request, pk):
    obj = get_object_or_404(Agent, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/agents/')


@login_required
def kbarticle_list(request):
    qs = KBArticle.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(title__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'kbarticle_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def kbarticle_create(request):
    if request.method == 'POST':
        obj = KBArticle()
        obj.title = request.POST.get('title', '')
        obj.category = request.POST.get('category', '')
        obj.content = request.POST.get('content', '')
        obj.views = request.POST.get('views') or 0
        obj.helpful_votes = request.POST.get('helpful_votes') or 0
        obj.status = request.POST.get('status', '')
        obj.save()
        return redirect('/kbarticles/')
    return render(request, 'kbarticle_form.html', {'editing': False})


@login_required
def kbarticle_edit(request, pk):
    obj = get_object_or_404(KBArticle, pk=pk)
    if request.method == 'POST':
        obj.title = request.POST.get('title', '')
        obj.category = request.POST.get('category', '')
        obj.content = request.POST.get('content', '')
        obj.views = request.POST.get('views') or 0
        obj.helpful_votes = request.POST.get('helpful_votes') or 0
        obj.status = request.POST.get('status', '')
        obj.save()
        return redirect('/kbarticles/')
    return render(request, 'kbarticle_form.html', {'record': obj, 'editing': True})


@login_required
def kbarticle_delete(request, pk):
    obj = get_object_or_404(KBArticle, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/kbarticles/')


@login_required
def settings_view(request):
    return render(request, 'settings.html')


@login_required
def api_stats(request):
    data = {}
    data['ticket_count'] = Ticket.objects.count()
    data['agent_count'] = Agent.objects.count()
    data['kbarticle_count'] = KBArticle.objects.count()
    return JsonResponse(data)
