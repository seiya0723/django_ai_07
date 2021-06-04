from django.contrib import admin
from .models import Design

#↑モデルインポート。↓インポートしたモデルを管理サイトで扱う

admin.site.register(Design)
