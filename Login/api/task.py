#定义成员任务
"""
- POST /api/tasks/ — 创建任务
- GET /api/tasks/ — 获取所有任务
- POST /api/tasks/{id}/update/ — 更新任务状态
"""
import json
from django.http import JsonResponse
from Login.models import User, PersonalTask, StudyGroup
from commo.parse_json_request import parse_json_request
#通过用户id唯一标识用户
from commo.validate_request import api_view

#小组创建者创建小组公共任务，添加任务标题，任务描述，任务截止时间。小组任务默认全组人员共同参与
#暂时不做

#个人任务，对应数据类型的personalTask
"""
  - title: 字符串类型，任务名称。
  - description: 字符串类型，任务描述。
  - due_date: 时间戳类型，任务截止时间。
  - assigned_to: 外键，指向User模型，任务分配给的用户。
  - group: 外键，指向StudyGroup模型，任务所属小组。
  - status: 字符串类型，任务的状态（如待完成、进行中、已完成）。
- 功能：
  - 提供创建任务、任务分配、进度更新等功能。
"""

#创建个人任务
@api_view(['POST'])
def personlTask(request):
    """
    使用post方法将个人任务上传
    """
    data = parse_json_request(request)
    assigned_to_id = data.get('assigned_to')
    group_id = data.get('group')
    created_by_id = data.get('created_by')  # 获取创建者的用户 ID

    try:
        assigned_to = User.objects.get(ID=assigned_to_id)
        group = StudyGroup.objects.get(id=group_id)
        created_by = User.objects.get(ID=created_by_id)  # 获取创建者的用户对象

        # 创建新的任务对象
        PersonalTask.objects.create(
            title=data.get('title'),
            description=data.get('description'),
            # 截止时间
            due_date=data.get('due_date'),
            # 添加任务的用户
            assigned_to=assigned_to,
            # 任务所属小组
            group=group,
            # 新建的任务默认待完成
            status='pending',
            # 添加创建者
            created_by=created_by
        )
        # 返回成功响应
        return JsonResponse({'ret': 0, 'msg': 'success.'}, status=200)
    except User.DoesNotExist:
        if assigned_to_id is None:
            return JsonResponse({'ret': 1, 'msg': '分配给的用户 ID 未提供或用户不存在.'}, status=400)
        elif created_by_id is None:
            return JsonResponse({'ret': 1, 'msg': '创建者的用户 ID 未提供或用户不存在.'}, status=400)
        return JsonResponse({'ret': 1, 'msg': '用户不存在.'}, status=400)
    except StudyGroup.DoesNotExist:
        return JsonResponse({'ret': 1, 'msg': '小组不存在.'}, status=400)
    except Exception as e:
        return JsonResponse({'ret': 1, 'msg': f'任务创建失败: {str(e)}'}, status=400)

#获取个人所有任务
def listTask(request):
    #根据用户id确定assigned_to，查找到个人的所有创建的任务的信息
    assigned_to_uid = request.GET.get('id')
    try:
        assigned_to = User.objects.get(ID=assigned_to_uid)
        db_personaltask = PersonalTask.objects.filter(assigned_to=assigned_to)
        tasks_list = []
        for task in db_personaltask:
            tasklist = {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'due_date': task.due_date,
                'status': task.status,
                'created_at': task.created_at,
            }
            tasks_list.append(tasklist)
        return JsonResponse({
            'ret': 0,
            'msg': 'success',
            'data': {
                'tasks_list': tasks_list,
            }
        }, status=201)
    except User.DoesNotExist:
        return JsonResponse({'ret': 1, 'msg': '用户不存在.'}, status=400)
    except Exception as e:
        return JsonResponse({'ret': 1, 'msg': f'获取任务失败: {str(e)}'}, status=400)

#更新任务状态
@api_view(['POST'])
def updatestatus(request):
    """
    用户对自己的任务状态进行更新，从待完成改成已完成
    :param request:assigned_to,title,status
    :return:
    """
    data = parse_json_request(request)
    #根据用户id确定assigned_to，查找到个人的所有创建的任务的信息
    assigned_to_uid =data.get('id')
    task_title = data.get('title')
    new_status = data.get('status')
    try:
        assigned_to = User.objects.get(ID=assigned_to_uid)
        #根据id和标题找到那条任务记录
        db_personaltask = PersonalTask.objects.filter(assigned_to=assigned_to, title=task_title).first()
        if db_personaltask:
            db_personaltask.status = new_status
            db_personaltask.save()
            return JsonResponse({'ret': 0, 'msg': 'success.'}, status=201)
        else:
            return JsonResponse({'ret': 1, 'msg': '任务不存在.'}, status=400)
    except User.DoesNotExist:
        return JsonResponse({'ret': 1, 'msg': '用户不存在.'}, status=400)
    except Exception as e:
        return JsonResponse({'ret': 1, 'msg': f'更新任务状态失败: {str(e)}'}, status=400)