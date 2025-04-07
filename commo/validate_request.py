# 辅助函数：解析请求体
import json
from functools import wraps
from django.http import JsonResponse


def validate_request(request, allowed_methods):
    if request.method not in allowed_methods:
        return False, JsonResponse({'ret': 1, 'msg': f'{request.method} request not allowed.'}, status=405)

    try:
        if request.method == 'POST':
            data = json.loads(request.body)
        elif request.method == 'GET':
            data = request.GET.dict()

        if not data:
            return False, JsonResponse({'ret': 1, 'msg': '请添加请求参数.'}, status=400)
        return True, data
    except json.JSONDecodeError:
        return False, JsonResponse({'ret': 1, 'msg': 'Invalid JSON format.'}, status=400)
    except Exception as e:
        return False, JsonResponse({'ret': 1, 'msg': f'Error: {str(e)}'}, status=500)


def api_view(http_methods):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            valid, data = validate_request(request, http_methods)
            if not valid:
                return data

            try:
                return view_func(request, *args, **kwargs)
            except Exception as e:
                return JsonResponse({'ret': 1, 'msg': f'Error: {str(e)}'}, status=500)
        return _wrapped_view
    return decorator