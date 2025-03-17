from django.shortcuts import render
from  .serializers import ProfileSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from .serializers import CustomLoginSerializer
from rest_framework import generics, permissions
from .models import Profile
from .serializers import ProfileSerializer
# Create your views here.
# views.py
from rest_framework.generics import RetrieveUpdateAPIView

class CustomLoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CustomLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        # Générez un token ou utilisez une authentification appropriée
        return Response({'message': 'Connexion réussie'}, status=status.HTTP_200_OK)
class ProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

    def perform_update(self, serializer):
        instance = self.get_object()
        new_statut = serializer.validated_data.get('statut', instance.statut)
        
        # Réinitialisation des champs lors du changement de statut
        if new_statut != instance.statut:
            if new_statut == 'client':
                serializer.validated_data.update({
                    'qualification': None,
                    'certifications': None,
                    'marques_prioritaires': None,
                    'annees_experience': None
                })
            elif new_statut == 'technicien':
                serializer.validated_data['marques_prioritaires'] = None
            elif new_statut == 'commerçant':
                serializer.validated_data.update({
                    'qualification': None,
                    'certifications': None
                })
        
        serializer.save()

# views.py
from rest_framework.views import APIView

class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        profile = request.user.profile
        
        if profile.statut == 'technicien':
            return Response({'dashboard': 'Technicien', 'data': ...})
        elif profile.statut == 'commercant':
            return Response({'dashboard': 'Commerçant', 'data': ...})
        else:
            return Response({'dashboard': 'Client', 'data': ...})
