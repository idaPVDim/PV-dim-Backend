# serializers.py
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import Profile
from django.contrib.auth import authenticate
from dj_rest_auth.serializers import LoginSerializer
from django.utils.translation import gettext as _
class CustomLoginSerializer(LoginSerializer):
    username = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'] = serializers.EmailField(required=True)
        self.fields['password'] = serializers.CharField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
            attrs['user'] = user
            return attrs

        msg = _('Must include "email" and "password".')
        raise serializers.ValidationError(msg, code='authorization')
class CustomRegisterSerializer(RegisterSerializer):
    nom = serializers.CharField()
    prenom = serializers.CharField()

    def get_cleaned_data(self):
        return {
            **super().get_cleaned_data(),
            'nom': self.validated_data.get('nom', ''),
            'prenom': self.validated_data.get('prenom', ''),
        }

# serializers.py
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
            'qualification': {'required': False},
            'certifications': {'required': False},
            'annees_experience': {'required': False},
            'marques_prioritaires': {'required': False}
        }

    def validate(self, data):
        statut = data.get('statut', self.instance.statut if self.instance else None)
        instance = self.instance if hasattr(self, 'instance') else None

        required_fields = []
        if statut == 'technicien':
            required_fields = ['qualification', 'certifications', 'annees_experience']
        elif statut == 'commerçant':
            required_fields = ['marques_prioritaires', 'annees_experience']

        errors = {}
        for field in required_fields:
            if field not in data:
                if instance and getattr(instance, field, None) is None:
                    errors[field] = _(f"Ce champ est requis pour le statut {statut}")
                elif not instance:
                    errors[field] = _(f"Ce champ est requis pour le statut {statut}")

        if errors:
            raise serializers.ValidationError(errors)
            
        return data