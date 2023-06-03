from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractUser



class UserManager(BaseUserManager):
    # 유저를 생성하는 함수
    def create_user(self, email, account, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        # 유저를 생성할 때, 입력해야 하는 값들 + 비밀번호는 무조건 입력해야함
        user = self.model(
            email=self.normalize_email(email),
            account=account,
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    # 슈퍼 유저를 생성하는 함수. python3 manage.py createsuperuser 할때
    def create_superuser(self, email, account, username, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        # 슈퍼 유저를 생성할 때, 입력해야 하는 값들 + 비밀번호는 무조건 입력해야함
        user = self.create_user(
            email,
            password=password,
            account=account,
            username=username,
        )
        user.is_admin = True # 슈퍼 유저는 관리자 권한이 있음
        user.save(using=self._db)
        return user


class User(AbstractUser):
    # 메타 클래스는, DB 정보들에 대한 정보를 입력하는 곳
    class Meta:
        db_table = "my_user" # DB 테이블 이름을 my_user 로 설정해줌

    email = models.EmailField(
        verbose_name='이메일',
        max_length=255,
        unique=True,
    )
    GENDERS = (
        ('Men', 'Men'),
        ('Women', 'Women'),
    )
    # Email , account 는 unique 해야 한다.
    account = models.CharField("계정이름", null=False, max_length=50, unique=True)
    age = models.PositiveIntegerField("나이", null=True)
    username = models.CharField("유저이름", null=False, blank=False, max_length=50)
    gender = models.CharField("성별", choices=GENDERS, max_length=10)
    introduction = models.TextField("자기소개", null=True, blank=True)
    profile_img = models.ImageField(
        "프로필 이미지",
        upload_to='users/%Y%m%d',
        # height_field=None,
        # width_field=None,
        # max_length=None,
        # default='static/img/die1_1.png',  # default 이미지
        # default='default/die1_1.png',  # default 이미지
        blank=True,
    )
    followings = models.ManyToManyField(
        "self", symmetrical=False, related_name='followers', blank=True)
        # symmetrical 대칭 여부 False, 팔로우와 팔로워가 필요충분은 아님
    created_at = models.DateField("계정 생성일", auto_now_add=True)
    is_active = models.BooleanField("활성화 여부", default=True)
    is_admin = models.BooleanField("관리자 여부", default=False)

    objects = UserManager() #쿼리셋 매니저가 UserManager임을 밝힘
    # USERNAME_FIELD 와 REQUIRED_FIELDS는 유저를 생성할 때, 필요한 필드이기 때문에 create_user 및 create_superuser시 필드를 추가시켜 줘야 함
    USERNAME_FIELD = 'account' # 회원가입시, 계정이름으로 가입하기 때문에, Unique=True 로 해주어야 하는 필드
    REQUIRED_FIELDS = ['email', 'username',]


    def __str__(self):
        return str(self.username)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
