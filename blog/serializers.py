from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils.timezone import now
from .models import Blog, Comment, Like, BlogView


class CommentSerializer(serializers.ModelSerializer):
    days_since_creation = serializers.SerializerMethodField()
    # PrimaryKeyRelatedField birden fazla tablo vs ile iliskisi var
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'blog', 'user', 'author', 'content',
                  'dateTime', 'days_since_creation')

    def get_days_since_creation(self, obj):
        return (now() - obj.dateTime).days

    def get_author(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name  # return obj.user.username

    def create(self, validated_data):
        user = self.context['request'].user
        if 'user' in validated_data:
            user = validated_data['user']
        return Comment.objects.create(user=user, **validated_data)


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    # likes = serializers.SerializerMethodField()  # 'no_likes_get'

    class Meta:
        model = Like
        fields = ('id', 'blog', 'user')

    # def no_likes_get(self, like_obj):
    #     return Like.objects.filter(post_id=like_obj.post_id).count()

    def create(self, validated_data):
        user = self.context['request'].user
        if 'user' in validated_data:
            user = validated_data['user']
        return Like.objects.create(user=user, **validated_data)


class BlogViewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = BlogView
        fields = ('id', 'blog', 'user')

    def create(self, validated_data):
        user = self.context['request'].user
        if 'user' in validated_data:
            user = validated_data['user']
        return BlogView.objects.create(user=user, **validated_data)


class BlogSerializer(serializers.ModelSerializer):
    days_since_creation = serializers.SerializerMethodField()
    dateTime = serializers.DateTimeField(write_only=True, required=False)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    author = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()
    likes = LikeSerializer(many=True, required=False)
    like_count = serializers.SerializerMethodField()
    views = BlogViewSerializer(many=True, write_only=True, required=False)
    view_count = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = ('id', 'user', 'author', 'title', 'content', 'image',
                  'dateTime', 'updatedTime', 'days_since_creation', 'category', 'likes', 'like_count', 'views', 'view_count', 'comments', 'comment_count')

    def get_days_since_creation(self, obj):
        return (now() - obj.dateTime).days

    def get_comment_count(self, obj):
        return obj.comments.count()

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_view_count(self, obj):
        return obj.views.count()

    def get_author(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name  # return obj.user.username

    def create(self, validated_data):
        user = self.context['request'].user
        if 'user' in validated_data:
            user = validated_data['user']
        return Blog.objects.create(user=user, **validated_data)
