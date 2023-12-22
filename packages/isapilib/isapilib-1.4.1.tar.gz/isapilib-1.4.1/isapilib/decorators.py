from django.http import JsonResponse

from isapilib.exceptions import SepaException


def safe_method(view_func):
    def wrapped_view(*args, **kwargs):
        try:
            return view_func(*args, **kwargs)
        except KeyError as e:
            return JsonResponse({
                'field': e.args[0],
                'message': f"This field is required."
            }, status=400)
        except SepaException as e:
            return JsonResponse({
                'field': 'Authentication',
                'message': str(e)
            }, status=401)

    return wrapped_view
