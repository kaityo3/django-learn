

from django import template
import datetime

register = template.Library()

@register.filter(name="past_time")
def culc_past_time(join_date):
    # joindatetime = datetime.datetime.strptime(join_date,"%Y/%m/%d")
    # 日付の差を計算
    date_difference = datetime.datetime.now() - join_date
    # 年と月に変換
    years = date_difference.days // 365
    remaining_days = date_difference.days % 365
    months = remaining_days // 30

    return (f"{years}年{months}ヶ月です。")
        
    
