import random

from django.core.validators import RegexValidator
from django.utils import timezone

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from ..shop.models import Book


class BookSerializer(serializers.ModelSerializer):
    """単一の本モデルオブジェクト用のシリアライザ"""

    class Meta:
        # 対象のモデルクラスを指定
        model = Book
        # 利用するモデルのフィールドを指定
        fields = ['id', 'title', 'price']
        # # 利用しないモデルのフィールドを指定
        # exclude = ['created_at']


class BookSerializer(serializers.ModelSerializer):
    """単一の本モデルオブジェクト用のシリアライザ"""

    class Meta:
        # 対象のモデルクラスを指定
        model = Book
        # 利用しないモデルのフィールドを指定
        exclude = ['created_at']

        # 3の方法:
        validators = [
            # タイトルと価格でユニークになっていることを検証
            UniqueTogetherValidator(
                queryset=Book.objects.all(),
                fields=('title', 'price'),
                message="タイトルと価格でユニークになっていなければいけません。"
            ),
        ]

        # 1の方法:
        extra_kwargs = {
            'title': {
                'error_messages': {
                    'blank': "タイトルは必須です。",
                },
            },
        }

        # 2の方法
        def validate_title(self, value):
            """タイトルに対するバリデーションメソッド"""
            if 'Java' in value:
                raise serializers.ValidationError(
                    "タイトルには「Java」を含めないでください。"
                )
            return value

        # 4の方法
        def validate(self, data):
            """複数フィールドに関係のあるバリデーションメソッド"""
            title = data.get('title')
            price = data.get('price')
            if title and '薄い本' in title and price and price > 3000:
                raise serializers.ValidationError(
                    "薄い本は3,000円を超えてはいけません。"
                )
            return data


class BookListSerializer(serializers.ListSerializer):
    """複数の本モデルオブジェクトを扱う用のシリアライザ"""

    # 対象のシリアライザを指定する
    child = BookSerializer()


class FortuneSerializer(serializers.Serializer):
    birth_date = serializers.DateField()
    blood_date = serializers.ChoiceField(choices=["A", "B", "O", "AB"])
    # 出力時にget_current_date()が呼ばれる
    current_date = serializers.SerializerMethodField()
    # 出力時にget_fortune()が呼ばれる
    fortune = serializers.SerializerMethodField()

    def get_current_date(self, obj):
        return timezone.localdate()

    def get_fortune(self, obj):
        seed = '{}{}{}'.format(timezone.localdate(), obj['birth_date'], obj['bood_type'])
        random.seed(seed)
        return random.choice(['大吉', '中吉', '小吉'])
