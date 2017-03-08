from django.contrib import admin

from .models import CategoryMemo

admin.site.register(CategoryMemo)

from .models import Memo
admin.site.register(Memo)