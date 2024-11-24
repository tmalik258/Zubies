from django.http import JsonResponse
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from .models import NewsLetter


@require_http_methods(["POST"])
@csrf_protect
def subscribe_view(request):
    """
    Handle newsletter subscription requests.
    Expects POST data with:
    - email: Valid email address
    - action: 'subscribe'
    """
    try:
        # Get POST data
        email = request.POST.get('email', '').strip().lower()
        action = request.POST.get('action')

        # Validate request
        if not email or action != 'subscribe':
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid request parameters'
            }, status=400)

        # Validate email format
        email_validator = EmailValidator()
        try:
            email_validator(email)
        except ValidationError:
            return JsonResponse({
                'status': 'error',
                'message': 'Please provide a valid email address'
            }, status=400)

        # Try to create or get subscriber
        subscriber, created = NewsLetter.objects.get_or_create(
            email=email,
            defaults={'subscribed': True}
        )

        if created:
            return JsonResponse({
                'status': 'success',
                'message': 'Congratulations and Welcome to Zubies\' Subscriber Family!',
                'created': True
            })
        else:
            # Handle existing subscriber
            if not subscriber.subscribed:  # If you have an subscribed field
                subscriber.subscribed = True
                subscriber.save()
                return JsonResponse({
                    'status': 'success',
                    'message': 'Your subscription has been reactivated!',
                    'reactivated': True
                })
            return JsonResponse({
                'status': 'info',
                'message': 'You are already subscribed to our newsletter!',
                'created': False
            })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': 'An error occurred while processing your request. Please try again.'
        }, status=500)