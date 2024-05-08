from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from base.models import create_id

# ＊カスタムユーザーモデルのドキュメント
# https://docs.djangoproject.com/ja/3.2/topics/auth/customizing/#a-full-example

#djangoが標準で用意しているuser modelをカスタマイズしている
class UserManager(BaseUserManager):
 
    # 一般userを作成するとき
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # superuserを作成するとき
    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username,
            email,
            password=password,
        )
        # admin権限=trueで管理者画面にアクセス可能
        user.is_admin = True
        user.save(using=self._db)
        return user
 

# userのコアな機能(権限やログインの際のe-mail情報の保存)
class User(AbstractBaseUser):
    # create_idを見えるようにして使用するため、idはランダム生成
    #create_idはmodels->item_models.pyの中でrandomに割り当てられるようになっているid
    id = models.CharField(default=create_id, primary_key=True, max_length=22)
    username = models.CharField(
        max_length=50, unique=True, blank=True, default='匿名')
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    # 管理画面にログインできるかどうか
    is_admin = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    # 必須項目はe-mail(usernameは任意)
    REQUIRED_FIELDS = ['email', ]
 
    def __str__(self):
        return self.email
 
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
 
# userデータ(コアなデータ)以外のある程度必要なデータについてはこちらに保存
class Profile(models.Model):
    # OneToOneFieldでUserインスタンスに1対1でデータが紐づくようにしている
    user = models.OneToOneField(
        # cascade : もし、あるUserインスタンスが削除されたら、このモデルも削除される
        User, primary_key=True, on_delete=models.CASCADE)

    # 以下の値はblank = Trueとなっており、入力せずとも問題ないようにはなっている
    # しかし注文する段階ではチェックが入るような仕様にする

    # 宛名(User.nameそのものでも特に問題ない)
    name = models.CharField(default='', blank=True, max_length=50)
    zipcode = models.CharField(default='', blank=True, max_length=8)
    prefecture = models.CharField(default='', blank=True, max_length=50)
    city = models.CharField(default='', blank=True, max_length=50)
    address1 = models.CharField(default='', blank=True, max_length=50)
    address2 = models.CharField(default='', blank=True, max_length=50)
    tel = models.CharField(default='', blank=True, max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return self.name
 
 
# Userモデルが作成されると同時に、OneToOneFieldが作成されるようにする
# @関数名 : デコレータ - あらかじめ定義された関数に@をつけて記述しその下にdef文を書くようにする
# そうするとdef文の処理をデコレータがさらに加工してデータを出力することが出来る

# post_save : djangoの機能で、usermodelが作られたことを検出する。
# post_saveを受け取った場合、reseiverが受け取り、その中で下のdef文の内容が処理される
@receiver(post_save, sender=User)
#**kwargsは可変長引数→辞書のような形でデータが渡ってる
def create_onetoone(sender, **kwargs):
    # もし、createdされていた場合、
    if kwargs['created']:
        # instansで渡っているuserでProfileクラスも作成されるということになる
        Profile.objects.create(user=kwargs['instance'])