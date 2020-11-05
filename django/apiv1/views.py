import logging

from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404

from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from rest_framework import generics

from ..shop.models import Book
from .serializers import BookSerializer

########################
# ModelViewSet
########################
from rest_framework import viewsets

from ..shop.models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    """本モデルのCRUD用APIクラス"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer


########################
# 汎用APIView
########################
# class BookCreateAPIView(generics.CreateAPIView):
#     """
#     本モデルの登録APIクラス
#     - create()を提供している
#     """
#     serializer_class = BookSerializer
#


logger = logging.getLogger(__name__)


class BookCreateAPIView(generics.CreateAPIView):
    """本モデルの登録APIクラス"""
    serializer_class = BookSerializer

    def create(self, request, *args, **kwargs):
        """本モデルの登録APIに対応するアクションメソッド"""
        response = super().create(request, *args, **kwargs)
        logger.info("Book(id={})を登録しました。".format(response.data['id']))
        return response


class BookListAPIView(generics.ListAPIView):
    """
    本モデルの取得（一覧）APIクラス
    - この例ではフィルタリングのためにfilter_backendsで個別APIの拡張を行っている
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = '__all__'

class BookRetrieveAPIView(generics.RetrieveAPIView):
    """本モデルの取得（詳細）APIクラス"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookUpdateAPIVIew(generics.UpdateAPIView):
    """本モデルの更新・一部更新APIクラス"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDeleteAPIVIew(generics.DestroyAPIView):
    queryset = Book.objects.all()


########################
# 普通のAPIView
#######################
class BookFilter(filters.Filterset):
    """本モデル用のフィルタクラス"""

    class Meta:
        model = Book
        fields = '__all__'


class BookListAPIView(views.APIView):
    """本モデルの取得（一覧）クラス"""

    def get(self, request, *args, **kwargs):
        """本モデルの取得（一覧）APIに対応するハンドラメソッド"""

        # モデルオブジェクトをクエリ文字列を使ってフィルタリングした結果を取得
        filterset = BookFilter(request.query_params, queryset=Book.objects.all())
        if not filterset.is_valid():
            # クエリ文字列のバリデーションがNGの場合は400エラー
            raise ValidationError(filterset.errors)
        # シリアライザオブジェクトを作成
        serializer = BookSerializer(instance=filterset.qs, many=True)
        # レスポンスオブジェクトを作成して返す
        return Response(serializer.data, status.HTTP_200_OK)


class BookRetrieveAPIView(views.APIView):
    """本モデルの取得（詳細）APIクラス"""

    def get(self, request, pk, *args, **kwargs):
        """本モデルの取得（詳細）APIに対応するハンドラメソッド"""

        # モデルオブジェクトを取得
        book = get_object_or_404(Book, pk=pk)
        # シリアライザオブジェクトを作成
        serializer = BookSerializer(instance=book)
        # レスポンスオブジェクトを作成して返す
        return Response(serializer.data, status.HTTP_200_OK)


class BookCreateAPIView(views.APIView):
    """本モデルの登録APIクラス"""

    def post(self, request, *args, **kwargs):
        """本モデルの登録APIに対応するハンドラメソッド"""

        # シリアライザオブジェクトを作成
        serializer = BookSerializer(data=request.data)
        # バリデーションを実行
        serializer.is_valid(raise_exception=True)
        # モデルオブジェクトを登録
        serializer.save()
        # レスポンスオブジェクトを作成して返す
        return Response(serializer.data, status.HTTP_201_CREATED)


class BookUpdateAPIView(views.APIView):
    """本モデルの更新・一部更新APIクラス"""

    def put(self, request, pk, *args, **kwargs):
        """本モデルの更新APIに対応するハンドラメソッド"""

        # モデルオブジェクトを取得
        book = get_object_or_404(Book, pk=pk)
        # シリアライザオブジェクトを作成
        serializer = BookSerializer(instance=book, data=request.data)
        # バリデーションを実行
        serializer.is_valid(raise_exception=True)
        # モデルオブジェクトを更新
        serializer.save()
        # レスポンスオブジェクトを作成して返す
        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request, pk, *args, **kwargs):
        """本モデルの一部更新APIに対応するハンドラメソッド"""

        # モデルオブジェクトを取得
        book = get_object_or_404(Book, pk=pk)
        # シリアライザオブジェクトを作成
        serializer = BookSerializer(instance=book, data=request.data, partial=True)
        # バリデーションを実行
        serializer.is_valid(raise_exception=True)
        # モデルオブジェクトを更新
        serializer.save()
        # レスポンスオブジェクトを作成して返す
        return Response(serializer.data, status.HTTP_200_OK)


class BookDeleteView(views.APIView):
    """本モデルの削除APIクラス"""

    def delete(self, request, pk, *args, **kwargs):
        """本モデルの削除APIに対応するハンドラメソッド"""

        # モデルオブジェクトを取得
        book = get_object_or_404(Book, pk=pk)
        # モデルオブジェクトを削除
        book.delete()
        # レスポンスオブジェクトを取得して削除
        return Response(status=status.HTTP_204_NO_CONTENT)
