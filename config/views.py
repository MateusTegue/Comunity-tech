from django.http import JsonResponse


def welcome_view(request):
    """Vista de bienvenida para la raíz del API"""
    return JsonResponse({
        'message': 'Bienvenido a ComunityTech API',
        'version': '1.0.0',
        'status': 'active'
    })

