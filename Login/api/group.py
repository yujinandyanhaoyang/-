#在这个文件里面定义学习小组
"""
1. 创建学习小组：用户通过POST请求创建学习小组，提供小组名称和描述，后端会返回小组的相关信息。
2. 加入学习小组：用户通过POST请求加入已有的小组，后端会将用户加入到指定的小组。
3. 查看小组成员：用户可以通过GET请求查看小组成员列表，返回成员的基本信息（如用户名、头像、简介等）。
4. 查看小组讨论内容：用户可以查看小组内的讨论内容，包括讨论的ID、发起者、内容和创建时间等信息。
"""
import json

from django.http import JsonResponse

from Login.models import StudyGroup, User, Resource, GroupDiscussions
from commo.parse_json_request import parse_json_request
from commo.validate_request import api_view


#创建学习小组
@api_view(['POST'])
def create_group(request):
    """
    用户可以创建学习小组
    :param request:
    :return:
    """
    # 创建一个学习小组对象接收请求参数
    data = parse_json_request(request)
    if isinstance(data, JsonResponse):
        return data
    study_group = StudyGroup()
    study_group.name = data.get('name')
    study_group.description = data.get('description')
    # 获取创建者对象
    created_by_id = data.get('created_by')
    try:
        study_group.created_by = User.objects.get(ID=created_by_id)
        #保存小组对象
        study_group.save()
        return JsonResponse({'ret': 0,'msg': '小组创建成功.'}, status=201)
    except User.DoesNotExist:
        return JsonResponse({'ret': 1,'msg': '创建者不存在.'}, status=400)

#加入学习小组
def join_group(request):
    """
    用户可以加入学习小组
    :param request:
    :return:
    """
    #试试用post方法接收表单数据
    group_id = request.POST.get('group_id')
    user_id = request.POST.get('u_id')
    try:
        group = StudyGroup.objects.get(id=group_id)
        user = User.objects.get(ID=user_id)
        #将用户加入小组
        group.members.add(user)
        return JsonResponse({'ret': 0,'msg': '加入小组成功.'}, status=200)
    except StudyGroup.DoesNotExist:
        return JsonResponse({'ret': 1,'msg': '小组不存在.'}, status=400)

# 查看小组信息

def get_member(request):
    """
    接收学习小组id，查找对应记录，返回小组名，小组描述，小组成员名，小组成员的描述
    :return:
    """
    # 获取小组对象并进行异常处理
    group_id = request.GET.get('group_id')
    try:
        db_group = StudyGroup.objects.get(id=group_id)
        members = db_group.members.all()
        members_list = []
        for member in members:
            memberlist = {
                'membername': member.username,
                'bio': member.bio,
                'profile_image': member.profile_image
            }
            members_list.append(memberlist)
        return JsonResponse({
            'ret': 0,
            'msg': 'success',
            'data': {
                'groupname': db_group.name,
                'description': db_group.description,
                'memberlist': members_list
            }
        }, status=200)
    except StudyGroup.DoesNotExist:
        return JsonResponse({'ret': 1, 'msg': '小组不存在.'}, status=400)
    except Exception as e:
        return JsonResponse({'ret': 1, 'msg': f'发生错误: {str(e)}'}, status=400)


def add_discussion(request):
    """
    用户可以创建小组讨论
    :param request: 请求对象
    :return:
    """
    if request.method == 'POST':
        try:
            # 解析 JSON 格式的请求体
            data = json.loads(request.body)
            # 获取必要的参数
            group_id = data.get('group_id')
            title = data.get('title')
            content = data.get('content')
            created_by_id = data.get('created_by')

            # 检查参数是否存在
            if not group_id or not title or not content or not created_by_id:
                return JsonResponse({'ret': 1, 'msg': '缺少必要参数'}, status=400)

            # 获取小组和发起人对象
            try:
                group = StudyGroup.objects.get(id=group_id)
                created_by = User.objects.get(ID=created_by_id)
            except StudyGroup.DoesNotExist:
                return JsonResponse({'ret': 1, 'msg': '小组不存在'}, status=400)
            except User.DoesNotExist:
                return JsonResponse({'ret': 1, 'msg': '发起人不存在'}, status=400)

            # 创建新的讨论实例
            discussion = GroupDiscussions(
                title=title,
                content=content,
                group=group,
                created_by=created_by
            )
            # 保存到数据库
            discussion.save()

            return JsonResponse({'ret': 0, 'msg': '讨论创建成功', 'discussion_id': discussion.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'ret': 1, 'msg': '请求体不是有效的 JSON 格式'}, status=400)
    else:
        return JsonResponse({'ret': 1, 'msg': '只允许 POST 请求'}, status=405)



# 查看小组讨论内容
def discussions(request):
    """
    用户可以查看小组内的讨论内容，包括讨论的ID、发起者、内容和创建时间等信息。
    :param request:
    :return:
    """
    # 获取小组对象并进行异常处理
    group_id = request.GET.get('id')
    discussion_title = request.GET.get('title')
    try:
        db_discussion = GroupDiscussions.objects.get(group_id=group_id, title=discussion_title)
        comments = db_discussion.comments.all()
        comment_list = []
        for comment in comments:
            commentlist = {
                'membername': comment.user.username,
                'content': comment.content,
            }
            comment_list.append(commentlist)
        return JsonResponse({
            'ret': 0,
            'msg': 'success',
            'data': {
                'group_id': db_discussion.group.id,
                'title': db_discussion.title,
                'content': db_discussion.content,
                'created_by': db_discussion.created_by.username,
                'comment_list': comment_list,
            }
        }, status=200)
    except GroupDiscussions.DoesNotExist:
        return JsonResponse({'ret': 1, 'msg': '讨论话题不存在.'}, status=400)
    except Exception as e:
        return JsonResponse({'ret': 1, 'msg': f'发生错误: {str(e)}'}, status=400)
