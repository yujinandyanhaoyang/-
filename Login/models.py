from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser):
    ID = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=10, unique=True, null=False, blank=False)
    email = models.CharField(max_length=20, unique=True, null=False, blank=False)
    password = models.CharField(max_length=128)  # 增加长度以存储哈希密码
    # 头像图片url
    # 后面根据用户的图像位置填写上用户头像图片的地址
    profile_image = models.CharField(max_length=40)
    bio = models.CharField(max_length=100)

    ROLE_CHOICES = [
        ('0', '普通用户'),
        ('1', '管理员用户'),
    ]
    role = models.CharField(
        max_length=1,
        choices=ROLE_CHOICES,
        default='0',  # 默认角色为普通用户
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

class Resource(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.CharField(max_length=100)
    file = models.FileField(upload_to='resources/')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='resources')
    likes = models.ManyToManyField(User, related_name='liked_resources', blank=True)

    def get_like_count(self):
        """
        获取资源的点赞数量
        """
        return self.likes.count()

    def __str__(self):
        """
        返回资源的标题，方便在管理界面和调试时查看
        """
        return self.title

class Comment(models.Model):
    content = models.CharField(max_length=500, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='comments')

class StudyGroup(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(User, related_name='study_groups')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_study_groups')
#定义一张组内讨论表，存储小组讨论的历史记录
class GroupDiscussions(models.Model):
    """
    title: 讨论的主题，最大长度30
    created_by: 讨论的发起人，记录发起人id，外键, 关联user模型
    user: 外键，指向User模型，评论作者。
    created_at: 时间戳类型，评论创建时间。
    """
    title = models.CharField(max_length=30, null=False, blank=False)
    content = models.CharField(max_length=300, null=False, blank=False)
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, related_name='discussions')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_discussions')
    created_at = models.DateTimeField(auto_now_add=True)
    comments = models.ManyToManyField(Comment, related_name='discussions', blank=True)

#个人任务
class PersonalTask(models.Model):
    title = models.CharField(max_length=20, null=False, blank=False)
    description = models.CharField(max_length=200, null=False, blank=False)
    due_date = models.DateField()  # 如果只需要日期
    STATUS_CHOICES = [
        ('pending', '待完成'),
        ('in_progress', '进行中'),
        ('completed', '已完成'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
    )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)  # 添加创建时间字段