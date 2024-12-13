from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RouteViewSet, TicketViewSet, PaymentViewSet, book_ticket

router = DefaultRouter()
router.register(r'routes', RouteViewSet)
router.register(r'tickets', TicketViewSet)
router.register(r'payments', PaymentViewSet)



urlpatterns = [
    path('api/', include(router.urls)),
    path('api/book-ticket/<int:route_id>/', book_ticket, name='book_ticket'),


]
