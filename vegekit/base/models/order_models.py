from django.db import models
import datetime
from django.contrib.auth import get_user_model

 
def custom_timestamp_id():
    dt = datetime.datetime.now()
    # μ秒までの時間を返す
    return dt.strftime('%Y%m%d%H%M%S%f')
 

# 注文履歴db(後から変更することはあまりない)
class Order(models.Model):
    # idは作成される時刻となる
    id = models.CharField(default=custom_timestamp_id,
                          editable=False, primary_key=True, max_length=50)
    # 注文したuser(cascadeのため、ユーザー情報が消去されるとこのデータも消える)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    # user id編集不可
    uid = models.CharField(editable=False, max_length=50)
    # successビューに飛んだ時のみTrueとなる
    is_confirmed = models.BooleanField(default=False)
    # 金額
    amount = models.PositiveIntegerField(default=0)
    # 税込金額
    tax_included = models.PositiveIntegerField(default=0)
    # 幾つあるか分からないためjsonの値を渡す
    items = models.JSONField()
    # 注文した段階の住所
    shipping = models.JSONField()
    # 発送日
    shipped_at = models.DateTimeField(blank=True, null=True)
    # キャンセル日
    canceled_at = models.DateTimeField(blank=True, null=True)
    # 管理者のメモ
    memo = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return self.id