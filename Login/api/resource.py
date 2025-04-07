"""
2. 学习资源管理
- POST /api/resources/ — 上传学习资源
- GET /api/resources/{id}/ — 获取指定资源的详细信息
- POST /api/resources/{id}/comments/ — 发表评论
- POST /api/resources/{id}/like/ — 资源点赞
"""

from django.http import JsonResponse
from Login.models import Resource, User, Comment
from commo.parse_json_request import parse_json_request
from commo.validate_request import api_view



# 存储学习资源函数
def upload(request):
    """
    用户可以上传PDF、Word、视频文件
    后端程序将这些学习资料存储到数据库
    :param request: 请求体中包含资源的标题，资源描述，文件，资源发布者
    :return:
    """
    # 从 request.POST 获取文本字段
    title = request.POST.get('title')
    description = request.POST.get('description')
    created_by_id = request.POST.get('created_by')

    if not title or not description or not created_by_id:
        return JsonResponse({'ret': 1, 'msg': '标题、描述和创建者 ID 是必需的.'}, status=400)

    try:
        created_by = User.objects.get(ID=created_by_id)
    except User.DoesNotExist:
        return JsonResponse({'ret': 1, 'msg': '创建者不存在.'}, status=400)

    # 处理文件上传
    if 'file' in request.FILES:
        file = request.FILES['file']
    else:
        return JsonResponse({'ret': 1, 'msg': '请上传文件.'}, status=400)

    # 创建一个资料对象接收请求参数
    resource = Resource()
    resource.title = title
    resource.description = description
    resource.created_by = created_by
    resource.file = file

    # 保存资源对象
    resource.save()

    return JsonResponse({'ret': 0, 'msg': '资源上传成功.'}, status=201)


# 获取指定资源详细信息
def get_resource_detail(request):
    """
    接收资源的 id 返回资源的详细信息
    :param request: 请求对象
    :param id: 资源的 id
    :return:
    """
    try:
        id = request.GET.get('id')
        # 尝试从数据库中查找对应的学习资料
        db_resource = Resource.objects.get(id=id)
        return JsonResponse({
            'ret': 0,
            'msg': 'success',
            'data': {
                'title': db_resource.title,
                'description': db_resource.description,
                'create_by': db_resource.created_by.username  # 假设返回用户名
            }
        })
    except Resource.DoesNotExist:
        return JsonResponse({'ret': 1, 'msg': '文件不存在.'}, status=400)

# 发表评论
@api_view(['POST'])
def addcomments(request):
    """
    使用POST发送评论信息
    :param request:
    :param id: 资源的 id
    :return:
    """
    data = parse_json_request(request)
    if isinstance(data, JsonResponse):
        return data
    # 获取用户 ID
    user_id = data.get('user')

    if not user_id:
        return JsonResponse({'ret': 1, 'msg': '用户 ID 缺失.'}, status=400)

    try:
        user = User.objects.get(ID=user_id)
    except User.DoesNotExist:
        return JsonResponse({'ret': 1, 'msg': '用户不存在.'}, status=400)

    try:
        resource = Resource.objects.get(id=user_id)
    except Resource.DoesNotExist:
        return JsonResponse({'ret': 1, 'msg': '资源不存在.'}, status=400)

    # 获取评论内容
    content = data.get('content')
    if not content:
        return JsonResponse({'ret': 1, 'msg': '评论内容不能为空.'}, status=400)

    # 创建评论对象
    Comment.objects.create(
        content=content,
        user=user,
        resource=resource
    )

    # 返回成功响应
    return JsonResponse({'ret': 0, 'msg': '评论发表成功.'}, status=200)

# 资源点赞
@api_view(['POST'])
def likes(request):
    """
    对资源进行点赞
    :param request:
    :param id: 资源的 id
    :return:
    """
    data = parse_json_request(request)
    if isinstance(data, JsonResponse):
        return data
    # 获取用户 ID
    user_id = data.get('user')

    # 检查用户 ID 是否存在
    if not user_id:
        return JsonResponse({'ret': 1, 'msg': '用户 ID 缺失.'}, status=400)

    try:
        user = User.objects.get(ID=user_id)
    except User.DoesNotExist:
        return JsonResponse({'ret': 1, 'msg': '用户不存在.'}, status=400)

    try:
        resource = Resource.objects.get(id=user_id)
    except Resource.DoesNotExist:
        return JsonResponse({'ret': 1, 'msg': '资源不存在.'}, status=400)

    # 创建或更新点赞记录
    like, created = resource.likes.through.objects.get_or_create(user=user, resource=resource)
    if created:
        return JsonResponse({'ret': 0, 'msg': '点赞成功.'}, status=200)
    else:
        like.delete()
        return JsonResponse({'ret': 0, 'msg': '取消点赞成功.'}, status=200)

