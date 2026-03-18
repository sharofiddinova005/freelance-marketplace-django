from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models import Project, Bid, Contract, ChatMessage
from .forms import ProjectForm, BidForm
from itertools import chain
from operator import attrgetter


def project_list(request):
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'projects.html', {'projects': projects})


@login_required
def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.client = request.user
            project.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'create_project.html', {'form': form})



@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)

    # 1. Ma'lumotlarni olish
    bids = project.bids.all()
    chat_messages = project.messages.all()

    # 2. Ikkala modelni bitta ro'yxatga birlashtirish va vaqt bo'yicha saralash
    combined_list = sorted(
        chain(bids, chat_messages),
        key=attrgetter('created_at')
    )

    if request.method == "POST":
        if 'chat_submit' in request.POST:
            text = request.POST.get('chat_text')
            if text:
                ChatMessage.objects.create(project=project, user=request.user, text=text)
                return redirect('project_detail', pk=project.pk)

        elif 'bid_submit' in request.POST:
            price = request.POST.get('price')
            message = request.POST.get('message')
            if price and message:
                Bid.objects.create(project=project, freelancer=request.user, price=price, message=message)
                return redirect('project_detail', pk=project.pk)

    return render(request, 'project_detail.html', {
        'project': project,
        'combined_list': combined_list,  # Saralangan ro'yxat
    })


@login_required
def my_bids(request):
    bids = Bid.objects.filter(freelancer=request.user).order_by('-created_at')
    return render(request, 'my_bids.html', {'bids': bids})


@login_required
def my_projects(request):
    projects = Project.objects.filter(client=request.user).order_by('-created_at')
    return render(request, 'projects.html', {
        'projects': projects,
        'title': 'Mening loyihalarim'
    })


def contract_list(request):
    # Agar foydalanuvchi faqat o'z shartnomalarini ko'rishi kerak bo'lsa:
    # contracts = Contract.objects.filter(bidfreelancer=request.user) | Contract.objects.filter(projectclient=request.user)
    contracts = Contract.objects.all()
    return render(request, 'contracts.html', {'contracts': contracts})

@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})


@login_required
def send_message(request, project_id):
    if request.method == "POST":
        project = get_object_or_404(Project, id=project_id)
        text = request.POST.get('message_text')
        if text:
            # Xabarni bazaga saqlash
            # Message.objects.create(project=project, user=request.user, content=text)
            return redirect('project_detail', pk=project_id)
    return redirect('project_detail', pk=project_id)