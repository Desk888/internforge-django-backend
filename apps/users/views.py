from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import User
from apps.skills.models import UserSkill
from .serializers import UserSerializer
from apps.skills.serializers import UserSkillSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class UserSkillViewSet(viewsets.ModelViewSet):
    queryset = UserSkill.objects.all()
    serializer_class = UserSkillSerializer
    permission_classes = [IsAuthenticated]