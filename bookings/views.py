from rest_framework.viewsets import ModelViewSet
from .models import Route, Ticket, Payment
from .serializers import RouteSerializer, TicketSerializer, PaymentSerializer
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

class RouteViewSet(ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

class TicketViewSet(ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

@require_GET
def get_routes(request):
    from_location = request.GET.get('from_location', '')
    to_location = request.GET.get('to_location', '')
    date = request.GET.get('date', '')

    # Отримуємо всі маршрути
    routes = Route.objects.all()

    # Застосовуємо фільтри
    if from_location:
        routes = routes.filter(from_location__icontains=from_location)
    if to_location:
        routes = routes.filter(to_location__icontains=to_location)
    if date:
        routes = routes.filter(departure_time__date=date)

    # Підготовка даних для JSON-відповіді
    data = [
        {
            'id': route.id,
            'from_location': route.from_location,
            'to_location': route.to_location,
            'departure_time': route.departure_time,
            'arrival_time': route.arrival_time,
            'price': route.price,
        }
        for route in routes
    ]

    return JsonResponse({'routes': data})

from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Ticket

@require_POST
def book_ticket(request, route_id):
    route = get_object_or_404(Route, id=route_id)
    data = request.POST

    # Отримуємо дані з POST-запиту
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    seat_number = data.get('seat_number')

    if not all([first_name, last_name, email, seat_number]):
        return JsonResponse({'error': 'Всі поля повинні бути заповнені'}, status=400)

    # Створюємо квиток
    ticket = Ticket.objects.create(
        route=route,
        user=request.user if request.user.is_authenticated else None,
        seat_number=seat_number,
        status='booked',
        first_name=first_name,
        last_name=last_name,
        email=email,
    )

    return JsonResponse({'message': 'Квиток успішно заброньовано', 'ticket_id': ticket.id})
