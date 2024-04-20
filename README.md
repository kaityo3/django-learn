# djangoの構築

## 前置き
  **※`conda activate djangoenv`で環境を変更することを忘れない**

  **gitのpush時にinvalid credentialsとエラーを吐かれたら、以下のコマンドを実行してみる<br>`export GIT_ASKPASS=`**

pythonの環境パスは以下の通り
miniconda/envs内の環境毎のディレクトリに保存される
djangoenvの場合はここ
`~/miniconda3/envs/djangoenv/bin/python`

## djangoアプリ作成とurlディスパッチ
### djangoアプリ作成
1. `django-admin startproject プロジェクト名`<br>プロジェクトファイルが作成される<br>(この時点で、`python manage.py runserver`でサーバー起動が可能)
2. `python manage.py migrate`<br>manage.pyの情報に基づき、データベースが作成される<br>データベースの種類はsettings.pyのDATABASE項で設定
3. `python manage.py startapp app名`<br>基本的なアプリ(管理機能等)を自動で作成してくれる。
4. settings.pyのINSTALLED_APP定義に3.で作成されたAPPフォルダを追加する
5. 作成したフォルダのviews.pyに表示したい処理を記載する。
6. urls.pyを作成し"urlpatterns"にてviewsとそのurlを紐づける。<br>`path("sample1", views.sample1,name="sample1"),`
7. project/urls.pyの"urlpatterns"にて、app/urls.pyを紐づける <br>`path("template_app/", include("TemplateApp.urls")),`

※(settings.pyのROOT_URLCONF = "first_project.urls"→first_project/urls.py→first_app/urls.pyのviews.index→views.pyのdef index()というイメージ)
### urlディスパッチ
- app/urls.pyのurlpatternsにおいて以下記述でurlの情報を引数に取ることが出来る<br>`path("add/<int:num1>/<str:num2>", views.add_page,name="add_page"),`
- 取得した引数は以下のように使用できる
```
views.py:

def add_page(request, num1, num2):
    return HttpResponse(f"<h1>{num1}+{num2}={num1+num2} add_page</h1>")
```
## viewとtemplateの連携
### django templateの利用とディレクトリ設定
djangoのviewsでhtmlを指定して呼び出すことが可能<br>その場合は、アプリケーションのフォルダにtemplateフォルダを作成してその中にhtmlを入れる。<br>その後以下のように記述する。
``` 
views.py:

def home(request):
    my_name = "Taro Yamada"
    favorite_fruits = ["Apple","Grape","Orange"]
    my_info = {
        "name": "murakami",
        "age": 28
    }
    # templateのhtmlに変数表示したい場合はcontextを使用してhtmlに与える
    return render(request,"home.html",context={
        "my_name": my_name,
        "favorite_fruits": favorite_fruits,
        "my_info": my_info
    })
```
contextにて与えられた変数を使用したhtml例
```
<h1>my name: {{ my_name }}</h1>
<h2>favorite_fruites: {{ favorite_fruits }}</h2>
<h2>age: {{ my_info.age }}</h2>
```

### staticを用いた性的コンテンツ利用
画像ファイルやcssを読み込むにはapp/staticフォルダを作成し、そこに画像やcssを入れる。  
※ファイル名に"download/"とあるが、これはsetting.pyのSTATICFILES_DIRSの指定によるものであることに注意する
```
{% load static %}
<link rel="stylesheet" type="text/css" href="{% static "download/home.css"%}">

<img src="{% static "download/sample.jpg" %}">
```
```
STATICFILES_DIRS = [
    ("download" , STATIC_DIR)
```

### templatesフォルダやstaticフォルダは他のフォルダから検索させることも可能<br>その場合は、settings.pyから以下の用にTEMPLATES-DIRSのリストに追加する。(上から順に検索される)
```
settings.py

import os
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = os.path.join(BASE_DIR,"templates")

-中略-

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATE_DIR,],
        -略-
    }
]

-中略-

STATICFILES_DIRS = [
    ("download" , STATIC_DIR)
]
```

### baseとなるhtmlをを引き継いだhtml作成
ページは特定のhtmlを派生させて記述することが可能  
再利用したい部分を`{% block ブロック名 %}{% endblock %}`で囲む
以下具体例
```
base.html:

<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>{% block title %}My Page{% endblock %}</title>
    </head>
    <body>
        <h1>My Page</h1>
            {% block content %}{% endblock %}
    </body>
</html>

```
引継ぎ先のhtmlでは、引継ぎ元を{% extends 引継ぎ元.html %}と記載し、
変更するblockのみ記載する
```
sample.html:

{% extends "base.html" %}
{% block title %}Sample1 {{ block.super }}{% endblock %}
{% block content %}
<p>Sample1</p>
{% endblock %}
```

### DTL(Django Template Language)の記法
- for,if文  以下のように{% %}で囲うことで、for,if文を実行可能
```

{# for #}
<ul>
{% for fruit in favorite_fruits %}
    <li>{{ fruit }}</li>
{% endfor %}
</ul>

{# if-endif #}
{% if "apple" in favorite_fruits %}
    <p>リンゴあります</p>
{% elif "grape" in favorite_fruits %}
    <p>ブドウあります</p>
{% else %}
    <p>Not Found</p>
{% endif %}

{% if my_info.age > 20 %}
    <p>成年済</p>
{% endif %}
```

### ページ間urlの記法
hrefタグに urlと記載した後、urls.pyで指定したapp_nameとurlpatternsのpathのnameを":"で繋ぐ  
また、変数を後続させるとスラッシュで区切られたurl内の変数として使用できる。(今回の場合はfirst_name,last_nameが変数)
```
<p><a href="{% url "template_app:home" first_name="minami" last_name="ando" %}">home</p>
# もし、変数をcontextとして渡されている場合、first_name = name といった記載も可能({{}}は不要)
```
これをクリックした際のリンク→http://127.0.0.1:8000/template_app/home/minami/ando
```
urls.py:

app_name = "template_app"
urlpatterns=[
    path("home/<first_name>/<last_name>", views.home,name="home"),
]
```
views.pyでは、取得した引数が使用出来るよう、引数に入れておく
```
def home(request, first_name, last_name):
-中略-
```


### フィルターの使い方
```
{# フィルター機能について #}
{# 大文字 #}
<h1>{{ name | upper }}</h1>
{# url化 #}
<h1>{{ page_url | urlize }}</h1>
{# 型変更 #} 
<p>BMI:{{ bmi | floatformat:2 }}</p>
{# デフォルト値設定 #}
<p>給料:{{ salary | default:"公開してません" }}</p>
{# リスト内ランダム表示 #}
<p>フルーツランダム {{ fluits | random | lower }}</p>
{# リスト内連結表示 #}
<p>フルーツリスト {{ fluits | join:"&" }}</p>
{# 改行含むメッセージ #}
<p>{{ msg | linebreaks }}</p>
{# 長いメッセージの省略 #}
<p>{{ msg2 | truncatechars:7 }}</p>

{# フィルターの全体適用 #}
{% filter upper %}
<p>aaa</p>
<h1>bbb</h1>
{% endfilter %}
```

### フィルターを自作することも可能
app/templatetagsに以下を配置
  - \_\_init__.py
  - event_tags.py

event_tags.pyには、デコレーターを用いて、filterに機能追加する  
statusはview.py側で定義しておく。("name"は後述)
```
event_tags.py:

from django import template

register = template.Library()

@register.filter(name="status_to_string")
def convert_status_to_string(status, name):
    print(f"name={name}")
    if status == 10:
        return "Success"
    elif status == 20:
        return "Error"
    elif status == 30:
        return "Pending"
    elif status == 40:
        return "Failed"
    else:
        return "Unknown"
```

呼び出すhtml側  
ここでfilter名の後に値を入れることで"name"という変数として使用可能となる
```
{% load event_tags %}
<p>{{ status | status_to_string:"Satoshi" }}</p>
```



## コマンド設定
|コマンド|説明|出展|
|:-------|----|:---|
|`ip a`|現在接続しているNetworkを確認する||
|`sudo wg`|VPN接続の状態を確認する||

## 初期設定方法
minicondaをインストールして、
`conda create -n djangoenv`を実行する
その後、`conda`コマンドで必要なパッケージをインストール

Ubuntuでsqlite3を覗くためにはsqlite3のinstallが必要らしい
sudo apt install sqlite3
