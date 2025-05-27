# KFGAPP/blogapp/views.py

from django.shortcuts import render, get_object_or_404, redirect # Added get_object_or_404
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.utils import timezone # For filtering by date
from django.views.generic import ListView # <<<<<<< ADD THIS IMPORT


# Updated model imports
from .models import Event, Category, Comment, EventImage # Import Event, EventImage instead of Post

def event_list(request):
    now = timezone.now()
    
    # Query for upcoming events
    upcoming_events_queryset = Event.objects.filter(
        status="scheduled",
        start_datetime__gte=now
    ).order_by('start_datetime')

    # Query for past events
    past_events_queryset = Event.objects.filter(
        status="scheduled", # Or perhaps also 'completed' if you use that status
        start_datetime__lt=now
    ).order_by('-start_datetime') # Show most recent past events first

    categories = Category.objects.filter(active=True)
    query = request.GET.get("q")

    # If there's a search query, apply it to both querysets (or decide if search only applies to upcoming)
    # For simplicity now, search will apply primarily to upcoming, or you might show a unified search result page.
    # Let's keep the search logic as it was, primarily affecting the main 'events' list, which we'll make 'upcoming'.
    
    active_events_list = upcoming_events_queryset # Default list to paginate and search
    page_title_suffix = "Upcoming Events"

    if query:
        active_events_list = active_events_list.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location_name__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
        page_title_suffix = f"Search Results for '{query}'"

    paginator = Paginator(active_events_list, 6) # Paginate by 6 (adjust as needed for horizontal cards)
    page_number = request.GET.get('page')
    upcoming_events_page_obj = paginator.get_page(page_number)

    # For past events, maybe show a limited number without pagination initially, or paginate separately later.
    # For now, let's just pass a slice of recent past events.
    recent_past_events = past_events_queryset[:3] 

    context = {
        "query": query,
        "categories": categories,
        "upcoming_events": upcoming_events_page_obj, # Paginated upcoming events
        "past_events": recent_past_events,          # A few recent past events
        "page_title": page_title_suffix,            # Dynamic page title
    }
    return render(request, 'events_list.html', context)

# vvvvvv THIS FUNCTION DEFINITION IS KEY vvvvvv
def event_detail(request, slug):
    event_obj = get_object_or_404(Event, slug=slug, status__in=["scheduled", "completed"])
    
    # Removed comment fetching and POST handling as per your request
    # For example, the 'comments' variable is no longer fetched here

    recent_events = Event.objects.filter(
        status="scheduled",
        start_datetime__gte=timezone.now()
    ).exclude(pk=event_obj.pk).order_by('start_datetime')[:5]

    related_events = []
    if event_obj.category:
        related_events = Event.objects.filter(
            category=event_obj.category,
            status="scheduled",
            start_datetime__gte=timezone.now()
        ).exclude(pk=event_obj.pk).order_by('start_datetime')[:4]

    event_obj.views += 1
    event_obj.save(update_fields=['views'])

    gallery_images = event_obj.gallery_images.all().order_by('uploaded_at')
    all_categories = Category.objects.filter(active=True)

    context = {
        "event": event_obj,
        "recent_events": recent_events,
        "related_events": related_events,
        "gallery_images": gallery_images,
        "categories": all_categories,
        "page_title": event_obj.title
        # Ensure 'comments' is NOT in context if you removed comment logic
    }
    # TEMPLATE LOCATION:
    # Since you confirmed 'event_detail.html' is in the project-level 'templates/' dir:
    return render(request, 'event_detail.html', context)
# ^^^^^^ END OF event_detail FUNCTION ^^^^^^

def all_past_events(request):
    now = timezone.now()
    past_events_queryset = Event.objects.filter(
        status__in=["scheduled", "completed"], # Include completed if you use that status
        start_datetime__lt=now
    ).order_by('-start_datetime') # Show most recent past first

    query = request.GET.get("q")
    if query: # Allow searching within past events too
        past_events_queryset = past_events_queryset.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location_name__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()

    paginator = Paginator(past_events_queryset, 9) # Paginate by 9 (e.g., 3x3 grid or 9 list items)
    page_number = request.GET.get('page')
    past_events_page_obj = paginator.get_page(page_number)

    context = {
        "query": query,
        "past_events_page": past_events_page_obj, # Note the different context variable name
        "page_title": "Past Events Archive"
    }
    # You'll need a new template for this page
    return render(request, 'all_past_events.html', context)

# vvvvvv ADD THIS CLASS-BASED VIEW FOR SEARCH vvvvvv
class EventSearchView(ListView):
    model = Event
    # TEMPLATE NAME FOR SEARCH RESULTS:
    # This template will display the search results.
    # Based on your structure, it might be 'users/templates/search_results.html'
    # or 'templates/search_results.html'
    template_name = 'search_results.html' # We'll create this template file later
    context_object_name = 'events'      # Variable name for the list of events in the template
    paginate_by = 10                    # Number of results per page

    def get_queryset(self):
        query = self.request.GET.get('q', None) # Get the search query 'q' from URL parameters
        if query:
            # Search in title, description, location, and tags
            # Only show 'scheduled' events that are upcoming or ongoing
            return Event.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(location_name__icontains=query) |
                Q(tags__name__icontains=query), # Assumes you have 'tags' TaggableManager on Event model
                status='scheduled',
                start_datetime__gte=timezone.now()
            ).distinct().order_by('start_datetime')
        return Event.objects.none() # If no query, return no results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_param = self.request.GET.get('q', '')
        context['page_title'] = f"Search Results for '{query_param}'"
        context['query'] = query_param # Pass the query back to the template to display in search box
        return context
# ^^^^^^ END OF EventSearchView CLASS ^^^^^^

# Note on template paths:
# I've used 'blogapp/template_name.html'.
# If your templates are directly in the project's 'templates/' folder (e.g., 'KFGAPP/templates/events_list.html'),
# then change the paths in render() to, e.g., 'events_list.html'.
# The typical Django best practice is to namespace templates within an app directory:
# KFGAPP/blogapp/templates/blogapp/events_list.html
# And then in settings.py, your DIRS for templates would be [BASE_DIR / 'templates'],
# and APP_DIRS should be True.
# For now, I'm assuming your templates might be directly in the project root `templates` or
# you want to organize them under `blogapp` (e.g. `templates/blogapp/`).
# Let's clarify your template structure if these paths cause "TemplateDoesNotExist".