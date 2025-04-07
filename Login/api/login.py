#定义用户的认证与信息管理操作
import json

from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, JsonResponse
from Login.models import User

#用户注册
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username').lower()
            password = data.get('password')
            email = data.get('email')

            if not username or not password or not email:
                return JsonResponse({'ret': 1, 'msg': 'Username, Email and password are required.'}, status=400)
            # 检查用户名或邮箱是否已存在
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                return JsonResponse({'ret': 1, 'msg': 'Username or Email already exists.'}, status=400)
            user = User()
            user.username = username
            user.password = make_password(password)  # 使用哈希处理密码
            user.email = email
            user.bio = data.get('bio', '')
            # 注册时设置用户为活跃状态
            user.is_active = True
            user.save()

            return JsonResponse({'ret': 0, 'msg': 'User registered successfully.'}, status=201)
        except Exception as e:
            return JsonResponse({'ret': 1, 'msg': f'Registration failed: {str(e)}'}, status=400)
    else:
        return JsonResponse({'ret': 1, 'msg': 'Only POST method is allowed.'}, status=405)

# 登录功能
def signin(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username_or_email = data.get('username_or_email')
            password = data.get('password')

            if not username_or_email or not password:
                return JsonResponse({'ret': 1, 'msg': '用户名/邮箱和密码是必需的。'}, status=400)

            username_or_email = username_or_email.lower()

            # 尝试用 username_or_email 作为用户名进行验证
            user = authenticate(request, username=username_or_email, password=password)

            if user is None and '@' in username_or_email:
                try:
                    user_by_email = User.objects.get(email__iexact=username_or_email)
                    print(f"通过邮箱找到用户: {user_by_email.username}")
                    print(f"用户密码: {user_by_email.password}")
                    print(f"请求密码: {password}")

                    # 使用 check_password 方法验证密码
                    password_matches = user_by_email.check_password(password)
                    print(f"使用 check_password 验证结果: {password_matches}")

                    user = authenticate(request, username=user_by_email.username, password=password)
                    print(f"通过邮箱验证: 输入 {user_by_email.username}, 结果 {user}")
                except User.DoesNotExist:
                    print(f"未找到邮箱为 {username_or_email} 的用户")
                    pass

            if user is not None:
                login(request, user)
                return JsonResponse({'ret': 0, 'msg': '登录成功。'}, status=200)
            else:
                return JsonResponse({'ret': 1, 'msg': '无效的用户名/邮箱或密码。'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'ret': 1, 'msg': '无效的 JSON 格式。'}, status=400)
        except Exception as e:
            return JsonResponse({'ret': 1, 'msg': f'错误: {str(e)}'}, status=500)
    else:
        return JsonResponse({'ret': 1, 'msg': '不允许使用 GET 请求。'}, status=405)

#获取用户信息
def listusermassage(request):
    if request.method == 'GET':
        try:
            user_id = request.GET.get('id')
            if not user_id:
                return JsonResponse({'ret': 1, 'msg': 'User ID is required.'}, status=400)

            try:
                user = User.objects.get(ID=user_id)
                return JsonResponse({
                    'username': user.username,
                    'profile_image': user.profile_image.url if user.profile_image else '',
                    'bio': user.bio,
                    'ret': 0,
                    'msg': 'Success'
                }, status=200)
            except User.DoesNotExist:
                return JsonResponse({'ret': 1, 'msg': 'User does not exist.'}, status=400)
        except Exception as e:
            return JsonResponse({'ret': 1, 'msg': f'Error: {str(e)}'}, status=500)
    else:
        return JsonResponse({'ret': 1, 'msg': 'Only GET method is allowed.'}, status=405)
