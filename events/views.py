from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from datetime import date
from .models import Event, Category, Participant

# Event Views
class EventListView(ListView):
    model = Event
    template_name = 'event_list.html'
    context_object_name = 'events'
    paginate_by = 10  # Adding pagination

    def get_queryset(self):
        queryset = Event.objects.select_related('category').prefetch_related('participants')

        # Get filter parameters from the request
        category_id = self.request.GET.get('category')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        # Filter by category if provided
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # Filter by date range if provided
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add categories to the context for the filter dropdown
        context['categories'] = Category.objects.all()
        return context


class EventCreateView(CreateView):
    model = Event
    fields = ['name', 'description', 'date', 'time', 'location', 'category']
    template_name = 'event_form.html'
    success_url = reverse_lazy('event-list')


class EventUpdateView(UpdateView):
    model = Event
    fields = ['name', 'description', 'date', 'time', 'location', 'category']
    template_name = 'event_form.html'
    success_url = reverse_lazy('event-list')


class EventDeleteView(DeleteView):
    model = Event
    template_name = 'event_confirm_delete.html'
    success_url = reverse_lazy('event-list')


# Participant Views
class ParticipantListView(ListView):
    model = Participant
    template_name = 'participant_list.html'
    context_object_name = 'participants'


class ParticipantCreateView(CreateView):
    model = Participant
    fields = ['name', 'email', 'events']
    template_name = 'participant_form.html'
    success_url = reverse_lazy('participant-list')

    def form_valid(self, form):
        participant = form.save()
        events = form.cleaned_data.get('events')
        if events:
            participant.events.set(events)  # Save ManyToMany relationships
        return redirect(self.success_url)


class ParticipantUpdateView(UpdateView):
    model = Participant
    fields = ['name', 'email', 'events']
    template_name = 'participant_form.html'
    success_url = reverse_lazy('participant-list')

    def form_valid(self, form):
        participant = form.save()
        events = form.cleaned_data.get('events')
        if events:
            participant.events.set(events)  # Update ManyToMany relationships
        return redirect(self.success_url)


# Dashboard View
def dashboard(request):
    today = date.today()

    total_participants = Participant.objects.count()
    total_events = Event.objects.count()
    upcoming_events = Event.objects.filter(date__gte=today).count()
    past_events = Event.objects.filter(date__lt=today).count()
    todays_events = Event.objects.filter(date=today)

    context = {
        'total_participants': total_participants,
        'total_events': total_events,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'todays_events': todays_events,
    }
    return render(request, 'dashboard.html', context)


# Search View
def search_events(request):
    query = request.GET.get('q', '')  # Get the search query from the request
    events = Event.objects.filter(
        Q(name__icontains=query) | Q(location__icontains=query)
    )  # Filter events by name or location (case-insensitive)
    return render(request, 'search_results.html', {'events': events, 'query': query})


# Category Views
class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'


class CategoryCreateView(CreateView):
    model = Category
    fields = ['name', 'description']
    template_name = 'category_form.html'
    success_url = reverse_lazy('category-list')


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'category_confirm_delete.html'
    success_url = reverse_lazy('category-list')
