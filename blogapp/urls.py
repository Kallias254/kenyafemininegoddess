# KFGAPP/blogapp/urls.py

from django.urls import path
from . import views # Use . to import from current app package

app_name = 'blogapp'

urlpatterns = [
    path('', views.event_list, name="event_list"),
    # path('category/<slug:category_slug>/', views.events_by_category, name="events_by_category"),

    # ADD THIS LINE FOR THE SEARCH FUNCTIONALITY
    path('search/', views.EventSearchView.as_view(), name="event_search"), # Using generic EventSearchView
    path('archive/past/', views.all_past_events, name="all_past_events"), # << NEW URL
    path('<slug:slug>/', views.event_detail, name="event_detail"),
    # Note: The detail view <slug:slug> should usually be last if it can match general strings,
    # to avoid it capturing 'search' or 'category'.
    # However, with distinct prefixes like 'search/' and 'category/', the order is less critical.
]