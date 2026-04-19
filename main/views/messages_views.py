from django.shortcuts import render

def messages_page(request):
    return render(request, 'messages/messages.html')