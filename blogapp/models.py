# blogapp/models.py (Refactored for Events)

from django.db import models
# from django.contrib.auth.models import User # Original import
from django.conf import settings # settings.AUTH_USER_MODEL might be used if you have a custom user
from django.contrib.auth import get_user_model # Preferred way to get the User model
from taggit.managers import TaggableManager
# from html import unescape # Not directly used in the new Event model's methods
# from django.utils.html import strip_tags # Not directly used in the new Event model's methods
from django.utils.text import slugify # For generating slugs
from django.urls import reverse # For get_absolute_url
from shortuuid.django_fields import ShortUUIDField
from ckeditor.fields import RichTextField

# Get the currently active User model
User = get_user_model()

# Define choices for Event status
# Renamed from BLOG_PUBLISH_STATUS and updated choices to be more event-relevant
EVENT_STATUS_CHOICES = (
    ("draft", "Draft"),                 # Event is being created, not yet visible
    ("scheduled", "Scheduled"),         # Event is planned and visible
    ("cancelled", "Cancelled"),         # Event has been cancelled
    ("completed", "Completed"),         # Event has already occurred (optional, for archiving)
    # ("in_review", "In Review"), # Kept if you have an approval workflow
)

class Category(models.Model):
    title = models.CharField(max_length=200)
    # Added blank=True to allow slug to be auto-generated in save method
    # Slug should be unique for categories
    slug = models.SlugField(unique=True, blank=True, max_length=220) # Increased max_length slightly
    active = models.BooleanField(default=True)

    class Meta:
        # ordering = ['-id'] # Original ordering
        ordering = ['title'] # Ordering alphabetically by title is often more user-friendly
        verbose_name = "Event Category" # Updated verbose name
        verbose_name_plural = "Event Categories" # Updated verbose name plural

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Auto-generate slug from title if it's not provided
        if not self.slug:
            self.slug = slugify(self.title)
            # Ensure uniqueness if titles can be similar (though slug is already unique=True)
            # This basic uniqueness check can be enhanced if needed for complex scenarios
            counter = 1
            original_slug = self.slug
            while Category.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    # Optional: Add a get_absolute_url if you have a page listing events by category
    # def get_absolute_url(self):
    #     return reverse('blogapp:category_event_list', kwargs={'category_slug': self.slug})


# Renamed from Post to Event
class Event(models.Model):
    # user: ForeignKey to the User model, representing the user who created/manages the event in the system.
    # Made it optional (null=True, blank=True) as events might be added by admins without a specific user account.
    # Renamed from 'user' to 'created_by_user' for clarity.
    created_by_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_events",
        help_text="The system user who created or is managing this event entry."
    )

    # Author (CharField from original Post model):
    # This seems to be for a display name if not linked to a system user.
    # Renamed to 'organizer_display_name' for clarity.
    organizer_display_name = models.CharField(
        max_length=255, # Original was 1000, 255 is usually sufficient for a name
        blank=True, # Can be blank if created_by_user is an organizer or if not applicable
        help_text="Publicly displayed name of the event organizer (e.g., a company, group, or individual)."
    )

    # featured_image = ImageField(blank=True, null=True, manual_crop="16:9", ...) # OLD Uploadcare field
    featured_image = models.ImageField(
        upload_to='event_featured_images/', # Images will be saved in MEDIA_ROOT/event_featured_images/
        blank=True,
        null=True,
        help_text="Main image for the event, displayed in listings and at the top of the event page."
    ) # NEW standard Django ImageField

    title = models.CharField(
        max_length=255, # Original was 1000, 255 is generally good for titles
        help_text="The official title of the event."
    )

    # slug: Added a slug field for user-friendly URLs.
    slug = models.SlugField(
        unique=True,
        blank=True, # Will be auto-generated
        max_length=275, # To accommodate longer titles
        help_text="URL-friendly version of the title (auto-generated)."
    )

    # content: Renamed to description. Using RichTextField for formatted content.
    # Removed max_length=50 from RichTextField as it's typically for TextField and 50 is too restrictive.
    description = RichTextField(
        help_text="Detailed information about the event. Use rich text for formatting."
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True, # Events might not always have a category
        help_text="Categorize the event (e.g., Workshop, Conference, Social)."
    )

    tags = TaggableManager(
        blank=True, # Tags can be optional
        help_text="Add tags to help users find the event (e.g., technology, music, free)."
    )

    # --- NEW EVENT-SPECIFIC FIELDS ---
    start_datetime = models.DateTimeField(
        help_text="Date and time when the event starts."
    )
    end_datetime = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date and time when the event ends (optional if it's a single point in time or all-day)."
    )
    location_name = models.CharField(
        max_length=255,
        help_text="Name of the venue or platform (e.g., 'Grand Ballroom', 'Online via Zoom', 'City Park')."
    )
    location_address = models.TextField(
        blank=True,
        null=True,
        help_text="Full street address if it's a physical location."
    )
    is_online_event = models.BooleanField(
        default=False,
        help_text="Check if this is primarily an online/virtual event."
    )
    registration_link = models.URLField(
        blank=True,
        null=True,
        help_text="Link to an external registration page, if any."
    )
    # ------------------------------------

    status = models.CharField(
        choices=EVENT_STATUS_CHOICES, # Using the new status choices
        max_length=100,
        default="draft", # Default to draft, so it's not public immediately
        help_text="Current status of the event."
    )
    featured = models.BooleanField(
        default=False,
        help_text="Check to mark this event as featured on the site."
    )
    # trending: Kept from original Post model. Could mean "popular" or "upcoming soon and highlighted".
    trending = models.BooleanField(
        default=False,
        help_text="Mark as a trending/popular event."
    )

    # date: Renamed to created_at for clarity on what this date represents.
    created_at = models.DateTimeField(auto_now_add=True)
    # Optional: Add an updated_at field
    updated_at = models.DateTimeField(auto_now=True)

    views = models.PositiveIntegerField(
        default=0,
        help_text="Number of times the event page has been viewed."
    )
    # pid: Kept ShortUUIDField from original Post model. Can serve as a stable internal ID.
    pid = ShortUUIDField(
        length=10,
        max_length=25,
        alphabet="abcdefghijklmnopqrstuvwxyz0123456789", # Added numbers for more combinations
        unique=True, # Ensure pid is unique
        help_text="Unique short ID for the event."
    )

    # Combined Meta classes from original Post model and updated for Event
    class Meta:
        # ordering = ['-date'] # Original ordering by 'date' (now 'created_at')
        ordering = ['start_datetime', 'title'] # Order by upcoming start date, then by title
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        # return self.title[0:10] # Original was very short
        return self.title

    def save(self, *args, **kwargs):
        # Auto-generate slug from title if it's not provided
        if not self.slug:
            self.slug = slugify(self.title)
            # Ensure uniqueness for the slug
            counter = 1
            original_slug = self.slug
            # Check against other Event objects, excluding self if this is an update
            queryset = Event.objects.filter(slug=self.slug)
            if self.pk:
                queryset = queryset.exclude(pk=self.pk)
            while queryset.exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
                queryset = Event.objects.filter(slug=self.slug) # Re-check with new slug
                if self.pk:
                    queryset = queryset.exclude(pk=self.pk)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # Assumes your URL pattern for event detail view is named 'event_detail'
        # and is in the 'blogapp' namespace (or whatever you name it).
        return reverse('blogapp:event_detail', kwargs={'slug': self.slug})

    # get_read_time(): This method was specific to blog post content length.
    # It's generally not applicable to events, so it's removed.
    # If you need a similar concept (e.g., estimated duration), it would be calculated differently,
    # likely from start_datetime and end_datetime.

    @property
    def is_past_due(self):
        """Checks if the event's start time has passed."""
        from django.utils import timezone
        if self.start_datetime:
            return self.start_datetime < timezone.now()
        return False


# NEW MODEL for Event Gallery Images
class EventImage(models.Model):
    event = models.ForeignKey(
        Event,
        related_name='gallery_images', # Used to access images from an Event instance (event.gallery_images.all())
        on_delete=models.CASCADE # If an event is deleted, its gallery images are also deleted
    )
    # image = ImageField( # Using Uploadcare ImageField
    #     manual_crop="4:3", # Example crop, adjust as needed
    #     help_text="Image for the event gallery."
    # )
    image = models.ImageField(
        upload_to='event_gallery_images/', # Images will be saved in MEDIA_ROOT/event_gallery_images/
        help_text="Image for the event gallery."
    ) # NEW standard Django ImageField
    caption = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Optional caption for the image."
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['uploaded_at']
        verbose_name = "Event Gallery Image"
        verbose_name_plural = "Event Gallery Images"

    def __str__(self):
        return f"Image for {self.event.title}" if self.event else "Orphaned Event Image"


# Comment model: Updated to link to Event instead of Post
class Comment(models.Model):
    event = models.ForeignKey( # Renamed from 'post' to 'event'
        Event,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) # Optional: Link comment to a logged-in user
    full_name = models.CharField(max_length=100) # Original was 1000, 100 is more typical for a name
    email = models.EmailField()
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True) # For moderation

    class Meta:
        ordering = ['-date']
        verbose_name = "Event Comment"
        verbose_name_plural = "Event Comments"

    def __str__(self):
        return f"Comment by {self.full_name} on {self.event.title}"[:60]


# StaticContent model: This seems independent of the blog/event functionality.
# It can remain as is, unless you want to rename sections or change its purpose.
# For now, I'm leaving it untouched.
class StaticContent(models.Model):
    SECTION_CHOICES = [
        ('about_us', 'About Us'),
        ('mission', 'Our Mission'),
        ('vision', 'Vision'),
        # You could add more generic sections here if needed
        # ('terms_of_service', 'Terms of Service'),
        # ('privacy_policy', 'Privacy Policy'),
    ]

    section_name = models.CharField(max_length=100, choices=SECTION_CHOICES, unique=True)
    content = RichTextField()

    def __str__(self):
        return self.get_section_name_display()

    class Meta:
        verbose_name = "Static Content Page"
        verbose_name_plural = "Static Content Pages"