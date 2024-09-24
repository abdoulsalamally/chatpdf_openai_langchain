from django.urls import path
from .views import home, chatbot, projects, upcoming_tools, billing, faq, contact, notifications, settings, profile, \
    terms, privacy, process_message, process_document_view, payment, notifications_details

app_name = 'dashboard'
urlpatterns = [
    path('home/', home, name='home'),
    path('chat/', chatbot, name='chat'),
    path('projects/', projects, name='projects'),
    path('upcoming-tools/', upcoming_tools, name='upcoming'),
    path('billing/', billing, name='billing'),
    path('faq', faq, name='faq'),
    path('contact/', contact, name='contact'),
    path('notifications', notifications, name='notifications'),
    path('settings/', settings, name='setttings'),
    path('profile', profile, name='profile'),
    path('terms', terms, name='terms'),
    path('privacy', privacy, name='privacy'),
    path('process-message', process_message, name='process-message'),
    path('process-document', process_document_view, name='process-document'),
    path('receivepayment/', payment, name='payment'),
    path('notification-details/<int:id>', notifications_details, name='notfication_details'),

]
