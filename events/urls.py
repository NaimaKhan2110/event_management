from django.urls import path
from .views import (
    EventListView, EventCreateView, EventUpdateView, EventDeleteView,
    ParticipantListView, ParticipantCreateView, ParticipantUpdateView,
    dashboard, search_events,
    CategoryListView, CategoryCreateView, CategoryDeleteView
)

urlpatterns = [
    # Event Management
    path('', EventListView.as_view(), name='event-list'),  # List all events
    path('event/new/', EventCreateView.as_view(), name='event-create'),  # Create a new event
    path('event/<int:pk>/edit/', EventUpdateView.as_view(), name='event-edit'),  # Edit an event
    path('event/<int:pk>/delete/', EventDeleteView.as_view(), name='event-delete'),  # Delete an event

    # Participant Management
    path('participants/', ParticipantListView.as_view(), name='participant-list'),  # List all participants
    path('participant/new/', ParticipantCreateView.as_view(), name='participant-create'),  # Create a new participant
    path('participant/<int:pk>/edit/', ParticipantUpdateView.as_view(), name='participant-edit'),  # Edit a participant

    # Dashboard
    path('dashboard/', dashboard, name='dashboard'),  # Dashboard view

    # Search
    path('search/', search_events, name='search-events'),  # Search functionality for events

    # Category Management
    path('categories/', CategoryListView.as_view(), name='category-list'),  # List all categories
    path('category/new/', CategoryCreateView.as_view(), name='category-create'),  # Create a new category
    path('category/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),  # Delete a category
]
