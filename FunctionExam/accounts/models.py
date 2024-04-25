from django.db import models
from django.contrib.auth.models import(
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from uuid import uuid4
from datetime import datetime, timedelta
from django.contrib.auth.models import UserManager


class Users(AbstractBaseUser, PermissionsMixin):
    # パスワードのフィールドはabstractbaseuserにあるので指定は不要
    username = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    email = models.EmailField(max_length=255, unique=True)
    # userが有効かどうか
    is_active = models.BooleanField(default=False)
    # 管理画面に入れるかどうか(PermissionsMixinにsuperuserか識別するフィールドがあるためここで記載せずともよい)
    is_staff = models.BooleanField(default=False)
    picture = models.FileField(null=True, upload_to="picture/")

    objects = UserManager()

    # このテーブルのレコードを一意に識別する決められた値。emailがuniqueなので、emailを指定する。
    USERNAME_FIELD = "email"
    # superuser作成時に入力するもの
    REQUIRED_FIELDS = ["username"]

    # managerとの関連付けに必須。この定義により上のclassのself.modelでこのUserを呼び出すことが出来る。"()必須"
    # objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = "users"


class UserActivateTokensManager(models.Manager):

    # UserActivateTokensのobjectsの機能を追加する
    def activate_user_by_token(self, token):
        # filterを実行し、tokenが一致していて"expired_at"__gte(現在より後)のデータを引っ張ってくる
        user_activate_token = self.filter(
            token=token,
            expired_at__gte=datetime.now()
        ).first()
        # リレーションされているuserを引っ張ってくる。
        user = user_activate_token.user
        # userのis_activeを有効化する
        user.is_active = True
        user.save()


class UserActivateTokens(models.Model):
    token = models.UUIDField(db_index=True)
    expired_at = models.DateTimeField()
    user = models.ForeignKey(
        "Users",on_delete=models.CASCADE
    )
    objects = UserActivateTokensManager()
    
    class Meta:
        db_table = "user_activate_tokens"

# Userのデータが作成されるたびに(post_save条件)、デコレータがついた関数(publish_token)が実行される。
@receiver(post_save, sender=Users)
def publish_token(sender, instance, **kwargs):
    # print(str(uuid4))
    # UserActivateTokensが実行される
    user_activate_token = UserActivateTokens.objects.create(
        user=instance, 
        token=str(uuid4()), 
        # 1日先の日付まで
        expired_at=datetime.now() + timedelta(days=1)
    )
    # メールでURLを送る方がよい
    print(f'http://127.0.0.1:8000/accounts/activate_user/{user_activate_token.token}')

