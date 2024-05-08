#  管理者画面の設定(管理画面で何を表示するかなど)

from django.contrib import admin
from base.models import Item,Category,Tag, User, Profile, Order
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from base.forms import UserCreationForm

#tag追加をadmin画面から見やすくする工夫
class TagInline(admin.TabularInline):
    model = Item.tags.through
class ItemAdmin(admin.ModelAdmin):
    inlines = [TagInline]
    exclude = ["tags"]

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
 
 
# Userモデルのどのような情報を表示するのかclassとして定義する
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        # 現在2段にしているが、別に1弾に全て表示しても構わない
        (None, {'fields': ('username', 'email', 'password',)}),
        (None, {'fields': ('is_active', 'is_admin',)}),
    )
 
    list_display = ('username', 'email', 'is_active',)
    list_filter = ()
    ordering = ()
    filter_horizontal = ()
    
    # 管理画面でuserを作成する際の設定項目の定義
    add_fieldsets = (
        (None, {'fields': ('username', 'email', 'is_active',)}),
    )
 
    # 管理画面上でもforms.pyの仕様を用いて、ユーザー作成ができる
    add_form = UserCreationForm
 
    # プロフィール情報もuserモデルと同じ場所に表示するようにする定義(profinlineの定義は上に記載)
    inlines = (ProfileInline,)


# ここに記載のあるものはadmin画面に表示される
admin.site.register(Order)
admin.site.register(Item,ItemAdmin)
admin.site.register(Category)
admin.site.register(Tag)
#初期表示のグループという枠を消す
admin.site.unregister(Group)
admin.site.register(User, CustomUserAdmin)