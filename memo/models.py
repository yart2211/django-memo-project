import uuid
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


class CategoryMemo(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


def uuid_defaults():
    return uuid.uuid4()


class Memo(models.Model):
    header = models.CharField(max_length=255)
    category = models.ForeignKey(CategoryMemo)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    content = models.TextField()
    is_favorite = models.BooleanField(default=False)
    date = models.DateTimeField('Время создания', default = datetime.now)
    uuid = models.CharField(max_length=36, default=uuid_defaults, unique=True)

    def __str__(self):
        return self.header








