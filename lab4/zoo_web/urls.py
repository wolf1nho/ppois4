from django.urls import path
from .views import (
    index,
    enclosures_page,
    enclosure_detail_page,
    staff_page,
    vet_logs_page,
    expositions_page,
    exposition_detail_page,
    tours_page,
    tour_detail_page,
    events_page,
    event_detail_page,
)

urlpatterns = [
    path('', index, name='index'),
    path('enclosures/', enclosures_page, name='enclosures'),
    path('enclosures/<int:enc_index>/', enclosure_detail_page, name='enclosure_detail'),
    path('staff/', staff_page, name='staff'),
    path('vet-logs/', vet_logs_page, name='vet_logs'),
    path('expositions/', expositions_page, name='expositions'),
    path('expositions/<int:exp_index>/', exposition_detail_page, name='exposition_detail'),
    path('tours/', tours_page, name='tours'),
    path('tours/<int:tour_index>/', tour_detail_page, name='tour_detail'),
    path('events/', events_page, name='events'),
    path('events/<int:event_index>/', event_detail_page, name='event_detail'),
]
