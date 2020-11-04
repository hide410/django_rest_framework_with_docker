import uuid
from django.utils import timezone

from django.db import models


class Publisher(models.Model):
    """出版社モデル"""

    class Meta:
        db_table = 'publisher'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name='出版社', max_length=20)
    created_at = models.DateTimeField(default=timezone.now)


class Book(models.Model):
    """本モデル"""

    class Meta:
        db_table = 'book'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(verbose_name='タイトル', max_length=20, unique=True)
    price = models.IntegerField(verbose_name='価格', null=True)
    publisher = models.ForeignKey(Publisher, verbose_name='出版社', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(default=timezone.now)
