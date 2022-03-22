from dataclasses import field, fields
from rest_framework import serializers, validators
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from dj_rest_auth.serializers import TokenSerializer


class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True,
        # UniqueValidator  kullaniyoruz cünkü iki farkli kullanici ayni emaille register olamasin diye
        validators=[validators.UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        # password frondenddte direkt görünmesin diye
        style={"input_type": "password"}
    )

    password2 = serializers.CharField(
        write_only=True,
        required=True,
        # password frondenddte direkt görünmesin diye
        style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = [
            #'id'
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'password2'
        ]
        extra_kwargs = {  # register old sonra kullanici frontend e bilgiler göndercem ama passwordleri degil. ondan writeonly yapiyoruz.
            'password': {'write_only': True},
            'password2': {'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.get('password')
        # pop methodu ile password2 yi yani belirtigimiz nesneyi listeden cikardik, yukarda fieldsten frontendten yani.
        validated_data.pop("password2")
        # **validated_data bu ciftyildiyli islem, kewwordargumetslerim  yani, keylerimi username vs i usermodelde eslestirip ona göre create eder.
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def validate(self, data):  # diğer validation'lar için dokümantasyonda serializer içerisindeki validation kısmını incele
        if data["password"] != data["password2"]:  # object-level validation
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return data


# class UserTokenSerializer(serializers.ModelSerializer)i üste yazdik cünkü üstten okuyup öyle degerlendiriyor
# Loginde token ile kullanıcı bilgilerini almak için
class UserTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email")


class CustomTokenSerializer(TokenSerializer):
    # Django yukarıdan aşağıya çalıştığı için UserTokenSerializer'ı yukarıda tanımlıyoruz.
    user = UserTokenSerializer(read_only=True)

    class Meta(TokenSerializer.Meta):
        fields = ("key", "user")  # key --> token
        # user'ın bilgilerini göndermek için user field'ını ekliyoruz.
