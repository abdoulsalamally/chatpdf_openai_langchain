import time
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from dashboard.models import TokenTracker, Notification
from core.calc_tokens import get_tokens
from core import chatpdf
from django.http import JsonResponse, HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from rave_python import Rave, RaveExceptions, Misc
from .models import Message
import json
from dotenv import load_dotenv
from django.views.decorators.http import require_POST

# Load environment variables
load_dotenv()

rave = Rave(os.getenv('RAVE_PUBLIC_KEY'), os.getenv('RAVE_SECRET_KEY'),
            usingEnv=True)



@login_required
def home(request):
    user_count = User.objects.count()

    context = {'user_count': user_count}
    return render(request, 'index-2.html', context)


@login_required
def chatbot(request):
    user = request.user
    token_tracker, created = TokenTracker.objects.get_or_create(user=user)
    token_tracker.save()

    context = {}

    return render(request, 'ai-chat-bot.html', context)


@login_required
def projects(request):
    context = {}

    return render(request, 'projects.html', context)


@login_required
def upcoming_tools(request):
    context = {}
    return render(request, 'upcoming-tools.html', context)


@login_required
def billing(request):
    if request.method == "POST":
        amount = int(request.POST['amount'])
        number = request.POST['number']
        email = request.POST['email']

        if amount >= 2000:

            # mobile payload
            payload = {
                "amount": amount,
                "email": email,
                "phonenumber": number,
                "redirect_url": "http://127.0.0.1:8000/receivepayment",
                "IP": ""
            }

            try:
                res = rave.UGMobile.charge(payload)

                if res['status'] == 'success':
                    print("HEHEHEHEHHEHEHEH")
                    return redirect(res['link'])


            except RaveExceptions.TransactionChargeError as e:
                print(e.err)
                print(e.err["flwRef"])

            except RaveExceptions.TransactionVerificationError as e:
                print(e.err["errMsg"])
                print(e.err["txRef"])
    context = {}
    return render(request, 'user-billing.html', context)


@login_required
def faq(request):
    context = {}
    return render(request, 'faq.html', context)


@login_required
def contact(request):
    context = {}
    if request.method == "POST":
        email = request.POST['email']
        message = request.POST['message']
        phone = request.POST['phone']
        con = Message.objects.create(user=request.user, email=email, phone=phone, message=message)

        con.save()

        return render(request, 'contact.html', context)

        # Give the user a message so that they can see that it is successful

    context = {}
    return render(request, 'contact.html', context)


@login_required
def notifications(request):
    nofts = Notification.objects.filter(user=request.user)
    context = {'notifications':nofts}
    return render(request, 'notifications.html', context)

@login_required
def notifications_details(request,id):
    nofts = Notification.objects.filter(id=id)
    context = {'notification':nofts[0]}
    return render(request, 'notification-single.html', context)

@login_required
def settings(request):
    context = {}

    if request.method == "POST":
        if request.POST.get('fname', None):
            fname = request.POST.get('fname', None)
            lname = request.POST.get('lname', None)
            username = request.POST.get('username', None)
            email = request.POST.get('email', None)

            user = request.user
            user.first_name = fname
            user.last_name = lname
            user.username = username
            user.email = email
            user.save()
            return redirect('/profile')
    return render(request, 'user-settings.html', context)


@login_required
def profile(request):
    context = {}
    return render(request, 'user-profile.html', context)


@login_required
def terms(request):
    context = {}
    return render(request, 'terms.html', context)


@login_required
def privacy(request):
    context = {}
    return render(request, 'privacy.html', context)


@login_required
@csrf_exempt
def process_message(request):
    if request.method == 'POST':
        print("##################")
        print(request.POST)
        try:
            request_data = json.loads(request.body.decode('utf-8'))
            user_message = request_data.get('userMessage', '')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON in the request'}, status=400)

        bot_response = chatpdf.process_prompt(user_message, request)
        data = {
            "botResponse": bot_response
        }

        json.dumps(data)

        return JsonResponse(data, status=200)


@login_required()
@csrf_exempt
def process_document_view(request):
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.FILES:
            return JsonResponse({
                "botResponse": "It seems like the file was not uploaded correctly, can you try "
                               "again. If the problem persists, try using a different file"
            }, status=400)

        uploaded_file = request.FILES['file']
        file_path = f'Media/{uploaded_file.name}'

        # Save the file
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # Process the document using the worker module (assuming 'worker' is properly imported)
        chatpdf.process_document(file_path, request, uploaded_file.name)

        # Return a success message as JSON
        return JsonResponse({
            "botResponse": "Thank you for providing your PDF document. I have analyzed it, so now you can ask me any "
                           "questions regarding it!"
        }, status=200)


@login_required
def payment(request):
    if request.method == 'GET':

        resp = request.GET['resp']
        print("xxxxxxxxxxxxxxxxxxxxxxx")
        print(resp)
        resp = json.loads(resp)
        state = resp['status']
        if state == 'success':
            amount = resp['data']['charged_amount']
            # Create the token object
            persons_tokens = TokenTracker.objects.get_or_create(user=request.user)[0]
            persons_tokens.token_count = persons_tokens.token_count + int((int(amount) / 2000) * 1000)
            persons_tokens.save()
            # Add the tokens to the person
            return redirect('/home/')

    return HttpResponse("Hello")
