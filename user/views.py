# django.shortcuts 에서 html을 보여주거나, url을 띄워주는 함수 import
# from django.shortcuts import redirect, render
# DRF 에 필요한 함수, 클래스 호출
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
# serializers 호출
from user.serializers import UserSerializer, CustomTokenObtainPairSerializer, UserProfileSerializer
from user.models import User



# 회원 가입시 토큰 생성
# from django.contrib.auth.tokens import PasswordResetTokenGenerator


# Create your views here.
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user = serializer.save()

            # 토큰 생성

            # uid = urlsafe_b64encode(force_bytes(user.pk))
            # token = PasswordResetTokenGenerator().make_token(user)

            return Response({"message": "가입완료!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)


# ====================== 프로필 상세보기 ================================
class ProfileView(APIView):
    def get_object(self, user_id):
        return get_object_or_404(User, id=user_id)

    # 프로필 상세보기, 권한이 없어도 됨.
    def get(self, request, user_id):
        user = self.get_object(user_id)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 프로필 수정, 권한이 있어야함.
    def patch(self, request, user_id):
        user = self.get_object(user_id)
        if user == request.user:
            serializer = UserProfileSerializer(
                user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "수정완료!"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "권한이 없습니다!"}, status=status.HTTP_403_FORBIDDEN)
# 이미지 업로드, 교체 가능, 삭제는 없음.


# ========================== 팔로우 =====================================
class FollowView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        you = get_object_or_404(User, id=user_id)
        serializer = UserProfileSerializer(you)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, user_id):
        you = get_object_or_404(User, id=user_id)
        me = request.user
        if me.is_authenticated:
            # 채연수정 : 현재 로그인한 유저와 팔로우 대상이 다를경우 (내가 아닌 경우에만 팔로우)
            # 준영 수정: Response가 잘못되어 수정하였습니다.
            if you != request.user:
                if me in you.followers.all():
                    you.followers.remove(me)
                    return Response("unfollow했습니다.", status=status.HTTP_200_OK)
                else:
                    you.followers.add(me)
                    return Response("follow했습니다.", status=status.HTTP_200_OK)
            else:
                return Response("자신을 팔로우 할 수 없습니다.", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("로그인이 필요합니다.", status=status.HTTP_403_FORBIDDEN)

# 로그인 한 유저만 팔로우 할 수 있게 수정함.
