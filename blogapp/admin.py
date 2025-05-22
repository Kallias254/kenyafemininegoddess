# KFGAPP/blogapp/admin.py

from django.contrib import admin
# Updated imports: Event, EventImage, Category, Comment, StaticContent
from .models import Event, EventImage, Category, Comment, StaticContent
from import_export.admin import ImportExportModelAdmin
from django.utils.html import format_html # For image thumbnail

# --- Inline Admin for Gallery Images within Event Admin ---
class EventImageInline(admin.TabularInline): # Or admin.StackedInline
    model = EventImage
    extra = 1 # Number of empty forms to display for new images
    readonly_fields = ('uploaded_at',) # Display upload time but don't allow editing
    # You can specify fields to display if you don't want all of them
    # fields = ('image', 'caption', 'uploaded_at')

    # If you want a thumbnail preview in the inline form (can make the form a bit tall)
    def image_preview(self, obj):
        if obj.image and hasattr(obj.image, 'url'): # Check if image exists and has a URL
            return format_html('<img src="{}" style="max-width: 150px; max-height: 100px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Preview'

    # Add 'image_preview' to readonly_fields if you use it and don't want it editable
    # Or add to 'fields' if you define a custom field layout
    # readonly_fields = ('uploaded_at', 'image_preview') # Example if adding preview here


# --- Admin Configuration for Event Model ---
# Renamed from ArticleAdmin to EventAdmin
class EventAdmin(ImportExportModelAdmin): # Retaining ImportExportModelAdmin functionality
    search_fields = ['title', 'description', 'organizer_display_name', 'location_name', 'tags__name']
    list_filter = ('category', 'status', 'featured', 'trending', 'is_online_event', 'start_datetime')
    list_display = (
        'title_display', # Using a custom method for potentially shorter title
        'status',
        'category',
        'start_datetime',
        'location_name',
        'featured',
        'trending',
        'created_by_user' # From the new Event model
    )
    # list_editable = ['status', 'category'] # Retained from ArticleAdmin, ensure fields are suitable
    # Be cautious with list_editable on fields that might have complex dependencies or validation.
    # For example, changing category or status might have other implications.

    prepopulated_fields = {'slug': ('title',)} # Added for slug generation

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'featured_image', 'description')
        }),
        ('Event Details', {
            'fields': ('start_datetime', 'end_datetime', 'location_name', 'location_address', 'is_online_event', 'registration_link')
        }),
        ('Organization & Categorization', {
            'fields': ('category', 'tags', 'organizer_display_name', 'created_by_user')
        }),
        ('Status & Visibility', {
            'fields': ('status', 'featured', 'trending')
        }),
    )
    readonly_fields = ('views', 'pid', 'created_at', 'updated_at') # Auto-managed fields
    inlines = [EventImageInline] # To manage gallery images

    def title_display(self, obj):
        # Provide a potentially shortened or more descriptive title for the list view
        return obj.title[:50] + '...' if len(obj.title) > 50 else obj.title
    title_display.short_description = 'Event Title' # Column header

    # If you had custom actions in ArticleAdmin, transfer them here if still relevant


# --- Admin Configuration for Category Model ---
# Kept similar to original, but ensure it matches the updated Category model
class CategoryAdmin(ImportExportModelAdmin):
    prepopulated_fields = {'slug': ('title',)} # Slug is now auto-generated in model, but prepopulate is good UX
    list_display = ('title', 'slug', 'active') # Added slug to list_display
    search_fields = ['title']
    list_filter = ('active',)


# --- Admin Configuration for Comment Model ---
# Updated to reflect changes in Comment model (linking to Event)
class CommentAdmin(ImportExportModelAdmin):
    search_fields = ['comment', 'full_name', 'email', 'event__title'] # Added search by event title
    list_editable = ('active',) # Retained from original
    list_filter = ('active', 'event__category') # Filter by active status and event's category
    list_display = ('comment_summary', 'full_name', 'event', 'active', 'date') # Changed 'post' to 'event'

    def comment_summary(self, obj):
        return obj.comment[:50] + '...' if len(obj.comment) > 50 else obj.comment
    comment_summary.short_description = 'Comment'

    actions = ['approve_comments', 'disapprove_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
    approve_comments.short_description = "Mark selected comments as Active"

    def disapprove_comments(self, request, queryset):
        queryset.update(active=False)
    disapprove_comments.short_description = "Mark selected comments as Inactive"


# --- Admin Configuration for EventImage Model (Optional: for direct management) ---
# This allows managing all gallery images in one place, outside of specific events.
class EventImageAdmin(ImportExportModelAdmin):
    list_display = ('get_event_title', 'caption', 'image_thumbnail', 'uploaded_at')
    list_filter = ('event__title', 'uploaded_at') # Filter by event title
    search_fields = ('caption', 'event__title')
    readonly_fields = ('uploaded_at',)

    def get_event_title(self, obj):
        return obj.event.title if obj.event else "No associated event"
    get_event_title.short_description = 'Event' # Column header
    get_event_title.admin_order_field = 'event__title' # Allows sorting by event title

    def image_thumbnail(self, obj):
        if obj.image and hasattr(obj.image, 'url'): # Check if image exists and has a URL
            # For pyuploadcare, the .url should give the direct URL to the image
            return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />', obj.image.url)
        return "No Image"
    image_thumbnail.short_description = 'Thumbnail'


# --- Admin Configuration for StaticContent Model ---
# Retained from your original, seems fine if StaticContent model is unchanged.
class StaticContentAdmin(admin.ModelAdmin): # Or ImportExportModelAdmin if you want export for this too
    list_display = ('section_name', 'get_content_summary')  # Display section name and content summary
    search_fields = ['section_name', 'content']  # Allow searching by section name and content
    fields = ('section_name', 'content') # Define fields for the edit form

    def get_content_summary(self, obj):
        # A helper to show a snippet of the RichTextField content
        from django.utils.html import strip_tags
        if obj.content:
            return strip_tags(obj.content)[:75] + '...' if len(strip_tags(obj.content)) > 75 else strip_tags(obj.content)
        return "N/A"
    get_content_summary.short_description = 'Content Summary'


# --- Registering Models with the Admin Site ---
# admin.site.unregister(Post) # If Post was ever registered and you want to be explicit, but it's not needed if Post model is gone
admin.site.register(Event, EventAdmin)          # Registering Event with EventAdmin config
admin.site.register(Category, CategoryAdmin)    # Registering Category
admin.site.register(Comment, CommentAdmin)      # Registering Comment
admin.site.register(EventImage, EventImageAdmin) # Registering EventImage (optional, if you want direct access)
admin.site.register(StaticContent, StaticContentAdmin) # Registering StaticContent