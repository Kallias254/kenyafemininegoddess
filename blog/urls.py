# KFGAPP/blog/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from graphene_django.views import GraphQLView # For GraphQL, if you're using it

# For user authentication views if defined directly at project level
# (though you also include('users.urls') which is good)
from users import views as user_views

urlpatterns = [
    # Third-party app URLs
    path('jet/', include('jet.urls', 'jet')),  # Django Jet URLS
    path('admin/', admin.site.urls),
    path('graphql/', GraphQLView.as_view(graphiql=True)), # If using GraphQL

    # User authentication and management URLs
    # These are defined directly here, which is fine.
    # They will take precedence if users.urls also defines them.
    path('register/', user_views.register, name='register'),
    path('login/', user_views.login, name='login'),
    path('logout/', user_views.logout, name='logout'),

    # Include URLs from the 'users' app (handles homepage, aboutus, etc.)
    # This is good, as it means URLs like /aboutus/ will be handled by users.urls
    path('', include(('users.urls', 'users'), namespace='users')), # Ensure namespace for users

    # Include URLs from the 'blogapp' (now for events)
    # Changed 'blogs/' to 'events/'
    path('events/', include('blogapp.urls')), # <--- KEY CHANGE HERE

    # It's good practice to ensure that ckeditor URLs are included if you use RichTextField
    # and haven't included it elsewhere (e.g., if ckeditor wasn't auto-discovered)
    # path('ckeditor/', include('ckeditor_uploader.urls')), # Add this if you use ckeditor image uploads and it's not working
]

# Serve media files during development
# This line is correctly placed and should remain
if settings.DEBUG: # Make sure this check is present
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # You might also need to serve static files this way if collectstatic isn't run often in dev,
    # but usually Django's runserver handles static files from app directories if APP_DIRS=True.
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)