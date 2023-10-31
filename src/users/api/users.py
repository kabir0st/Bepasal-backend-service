from core.utils.viewsets import DefaultViewSet
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.models import UserBase
from users.models.supports import VerificationCode
from .auth import authenticate_user
from .serializers.userbase import (RegisterUserBaseSerializer,
                                   UserBaseSerializer)
from rest_framework.decorators import action


class RegisterUserBaseAPI(GenericAPIView):
    serializer_class = RegisterUserBaseSerializer
    permission_classes = [AllowAny]
    http_method_names = ["post"]

    def post(self, request):
        data = request.data.copy()
        data['is_staff'] = False
        data['is_superuser'] = False

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            token, details = authenticate_user(request.data['email'],
                                               request.data['password'])
            VerificationCode.objects.create(email=data['email'])
            return Response({"tokens": token, "user_details": details})
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)


class UserBaseAPI(DefaultViewSet):
    serializer_class = UserBaseSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'
    search_fields = ["first_name", 'last_name', 'email']
    http_method_names = ["get", "patch", "delete"]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return UserBase.objects.filter().order_by('-id')
        return UserBase.objects.filter(id=self.request.user.id)

    @action(methods=['get'], detail=True)
    def verify(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.is_staff:
            obj.is_verified = not obj.is_verified
            obj.save()
        return Response({'status': True, 'msg': "Verification Successful."})
