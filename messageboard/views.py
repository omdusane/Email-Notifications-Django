from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MessageBoard
from .forms import *
from .tasks import send_email_task
from django.core.mail import EmailMessage

@login_required
def messageboard_view(request):
    messageboard = get_object_or_404(MessageBoard, id=1)
    form = MessageCreateForm()

    if request.method == 'POST':
        if request.user in messageboard.subscribers.all():
            form = MessageCreateForm(request.POST)
            if form.is_valid:
                message = form.save(commit=False)
                message.author = request.user
                message.messageboard = messageboard
                message.save()
                send_email(message)
        else:
            messages.warning(request, 'You must be a subscriber to access this messageboard.')

        return redirect('messageboard')
    context = {
        'messageboard': messageboard,
        'form': form,
    }
    return render(request, 'messageboard/index.html', context)

@login_required
def subscribe_view(request):
    messageboard = get_object_or_404(MessageBoard, id=1)

    if request.user not in messageboard.subscribers.all():
        messageboard.subscribers.add(request.user)
    else:
        messageboard.subscribers.remove(request.user)

    return redirect('messageboard')


def send_email(message):
    messageboard = message.messageboard
    subscribers = messageboard.subscribers.all()

    for subscriber in subscribers:
        subject = f'New message from {message.author.profile.name}'
        body = f'{message.author.profile.name} : {message.body} \n\n Regards from MessageBoard'

        send_email_task.delay(subject, body, subscriber.email)