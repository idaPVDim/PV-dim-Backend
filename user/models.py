# models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email obligatoire')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom']

    objects = CustomUserManager()

# models.py
class Profile(models.Model):
    STATUTS = (
        ('technicien', 'Technicien'),
        ('commercant', 'Commerçant'),
        ('client', 'Client')
    )
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    statut = models.CharField(max_length=20, choices=STATUTS)
    
    # Champs conditionnels
    qualification = models.CharField(max_length=100, blank=True, null=True)
    certifications = models.TextField(blank=True, null=True)
    annees_experience = models.IntegerField(blank=True, null=True)
    marques_prioritaires = models.TextField(blank=True, null=True)
