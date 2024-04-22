from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .forms import UserChangeForm, UserCreationForm
from .models import Students,Schools
from django.shortcuts import redirect

User = get_user_model()

# 管理画面の表示の仕方を変える(UserAdminのオーバーライドのため変数名等は注意)
class CustomizeUserAdmin(UserAdmin):
    form = UserChangeForm # ユーザ編集画面でつかうForm
    add_form = UserCreationForm # ユーザ作成画面

    # 一覧画面で表示する要素
    list_display = ("username", "email", "is_staff")
    # user情報修正画面で表示する要素
    fieldsets = (
        ('ユーザ情報', {'fields': ('username', 'email', 'password', 'website', 'picture')}),
        ('パーミッション', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )

    # user作成画面で表示する要素
    add_fieldsets = (
        ('ユーザ情報', {
            'fields': ('username', 'email', 'password', 'confirm_password')
        }),
    )

 
 
@admin.register(Students)
class StudentAdmin(admin.ModelAdmin):
    # 表示順を変更出来る。
    fields = ('name', 'score', 'age', 'school')
    # 生徒一覧の表示を変更出来る。
    list_display = ('id', 'name', 'age', 'score', 'school')
    # 編集画面に遷移するリンクのフィールドを変更する
    list_display_links = ('name',)
    # 検索できるフィールドを追加する(管理画面上に検索ボックスが表示されるようになる)
    search_fields = ('name', 'age')
    # リスト出来るフィールドを追加する(管理画面右にフィルターが表示されるようになる)
    list_filter = ('name', 'age', 'score', 'school')
    # 一覧画面上から値を修正できるようになる(list_display_linksに指定されたものは不可)
    list_editable = ('age', 'score', 'school')

    # "保存してもう一つ追加"の不具合の解消(djangoの新verからリストページにリダイレクトされてしまっている)
    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/admin/accounts/students/add/')
 
@admin.register(Schools)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("name","student_count")

    # objはschoolクラス1つ1つのインスタンス
    def student_count(self, obj):
        # print(type(obj))
        # print(dir(obj))
        count = obj.students_set.count()
        return count

    student_count.short_description = "生徒数"


admin.site.register(User, CustomizeUserAdmin)

# admin.site.register(Schools)


