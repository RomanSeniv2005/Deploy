from django.shortcuts import render
from django.views.generic import TemplateView
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from bookings.views import get_routes
from bookings.models import *
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.middleware.csrf import get_token


def ticket_list_view(request):
    response = requests.get('http://127.0.0.1:8000/api/tickets/')  # Вказуємо URL ендпоїнту
    tickets = response.json() if response.status_code == 200 else []
    return render(request, 'frontend/tickets.html', {'tickets': tickets})

class HomePageView(TemplateView):
    template_name = 'frontend/home.html'

class SignUpView(CreateView):
    template_name = 'frontend/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('signin')

from django.http import JsonResponse
import json

def route_list_frontend(request):
    response = get_routes(request)

    if response.status_code == 200:
        # Отримуємо дані з JsonResponse
        response_content = response.content
        routes_data = json.loads(response_content).get('routes', [])
    else:
        routes_data = []  # Якщо API не повернуло успішну відповідь

    return render(request, 'frontend/routes.html', {
        'routes': routes_data,
        'from_location': request.GET.get('from_location', ''),
        'to_location': request.GET.get('to_location', ''),
        'date': request.GET.get('date', ''),
    })



@login_required
def ticket_booking_page(request, route_id):
    route = get_object_or_404(Route, id=route_id)

    if request.method == 'POST':
        seat_number = request.POST.get('seat_number')
        first_name = request.POST.get('first_name', request.user.first_name)
        last_name = request.POST.get('last_name', request.user.last_name)
        email = request.POST.get('email', request.user.email)

        if not all([seat_number, first_name, last_name, email]):
            return render(request, 'frontend/ticket.html', {
                'route': route,
                'error_message': 'All fields are required.',
            })

        try:
            ticket = Ticket.objects.create(
                route=route,
                user=request.user,
                seat_number=seat_number,
                first_name=first_name,
                last_name=last_name,
                email=email,
                status='booked',
            )
            return render(request, 'frontend/booking_success.html', {'ticket': ticket})
        except Exception as e:
            return render(request, 'frontend/ticket.html', {
                'route': route,
                'error_message': f'Failed to book ticket: {str(e)}',
            })

    return render(request, 'frontend/ticket.html', {'route': route})
