from email.policy import default
from pyexpat import model
from unicodedata import category
from django.db import models
from django.utils.crypto import get_random_string
import os
from joblib import MemorizedResult

from pytest import Instance

def create_id():
    return get_random_string(22)

#instance Itemクラスのインスタンス
def upload_image_to(instance,filename):
    item_id = instance.id
    #static->item->item_idフォルダが作成され、最後にfilenameがその中に生成される
    return os.path.join('static','items',item_id,filename)

class Tag(models.Model):
    #id urlに表示する予定
    slug = models.CharField(max_length=32,primary_key=True)
    #日本語のカテゴリ名
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name    

#categoryクラスを作成(itemクラスで使用するから上に配置する)
class Category(models.Model):
    #id urlに表示する予定
    slug = models.CharField(max_length=32,primary_key=True)
    #日本語のカテゴリ名
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name



class Item(models.Model):
    #ID db上のidとするためにprimary_key = Trueとする
    #create_idは実行されていないので()を付けない
    id = models.CharField(default=create_id,primary_key=True,max_length=22,editable=False)
    name = models.CharField(default='', max_length=50)
    #PositiveInteger 正の整数
    price = models.PositiveIntegerField(default=0)
    stock = models.PositiveIntegerField(default=0)
    #textfield 長文を扱える、blank = trueで入っていなくても良い
    description = models.TextField(default='', blank=True)
    sold_count = models.PositiveIntegerField(default=0)
    #trueならそのアイテムが公開されるようになる
    is_published = models.BooleanField(default=False)
    #作成日
    created_at = models.DateTimeField(auto_now_add=True)
    #更新日
    updated_at = models.DateTimeField(auto_now=True)
    #defaultで空でもok,upload先はupload_to
    image = models.ImageField(default="", blank = True,upload_to = upload_image_to)
    #foreign key 1対多のリレーション構築が可能。ondeleteもしカテゴリが削除されたらnull値を入力する(models.kascadeでカテゴリが削除されたらアイテムを削除するなどもある)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True,blank=True)
    #tomanyfield 複数タグを参照可能。中間テーブルを挟んでリレーションされるためondeleteは不要
    tags = models.ManyToManyField(Tag)

    #ここにreturnしたものが、管理者画面でも表示される(print(Itemインスタンス)で指定した際に呼び出される名前)
    def __str__(self):
        return self.name
