from django.conf import settings


def branding(request):
    """Expose branding-related values to all templates."""
    return {
        'logo_url': getattr(settings, 'LOGO_URL', ''),
        'site_name': 'Great Owl Marketing',
        'static_version': getattr(settings, 'STATIC_VERSION', ''),
    }
