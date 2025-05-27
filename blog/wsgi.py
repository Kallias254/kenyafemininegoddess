# KFGAPP/blog/wsgi.py

import os
from django.core.wsgi import get_wsgi_application
from django.conf import settings # Import settings
from whitenoise import WhiteNoise # Import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')

# Get the standard Django WSGI application
application = get_wsgi_application()

# Wrap with WhiteNoise, first for static files (from STATIC_ROOT)
# WhiteNoise will automatically find files in settings.STATIC_ROOT
application = WhiteNoise(application, root=settings.STATIC_ROOT)

# Then, add files from MEDIA_ROOT to be served under MEDIA_URL
# This is only recommended for DEBUG=False environments where Django doesn't serve media.
# For high-traffic sites, a dedicated media server (S3, Nginx) is better.
if not settings.DEBUG: # Only add media serving by WhiteNoise if DEBUG is False
    application.add_files(settings.MEDIA_ROOT, prefix=settings.MEDIA_URL.strip("/"))

# Note: The original line `application = WhiteNoise(application, root=settings.STATIC_ROOT)`
# effectively does what `WhiteNoise(get_wsgi_application(), root=settings.STATIC_ROOT)` would do.
# The subsequent `application.add_files()` augments this WhiteNoise instance.