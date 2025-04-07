import json
from django.http import JsonResponse

def parse_json_request(request):
    """
    解析请求体中的 JSON 数据
    :param request: 请求对象
    :return: 解析后的 JSON 数据或错误响应
    """
    try:
        return json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'ret': 1, 'msg': '请求体不是有效的 JSON 格式.'}, status=400)