from .models import Editpage # Assuming Editpage is in users.models

def site_wide_content(request):
    footer_content = Editpage.objects.filter(section_name='footer').first()
    # You can add other site-wide data here too, e.g., social media links, site name
    return {
        'site_footer': footer_content, # Use a distinct name like 'site_footer'
    }