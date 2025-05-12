from django.conf import settings
from django.http import JsonResponse
from urllib.parse import urlparse


class DomainRestrictionMiddleware:
    """
    Blocks requests coming from untrusted domains.
    Compares against settings.TRUSTED_ORIGINS using Origin or Referer headers.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        origin_header = request.META.get('HTTP_ORIGIN') or request.META.get('HTTP_REFERER')
        
        if origin_header:
            parsed_origin = urlparse(origin_header)
            origin = f"{parsed_origin.scheme}://{parsed_origin.netloc}"
            print('Incoming request from:', origin)

            if origin not in settings.TRUSTED_ORIGINS:
                return JsonResponse({'error': 'Invalid request domain.'}, status=403)

        return self.get_response(request)