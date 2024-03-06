from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User

# Create your models here.
class Make(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.name

class Auto(models.Model):
    nickname = models.CharField(max_length=200)
    mileage = models.PositiveIntegerField()
    make = models.ForeignKey('Make', on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    user_specific_id = models.PositiveIntegerField()

    def __str__(self):
        return self.nickname
    
    def save(self, *args, **kwargs):
        if not self.id:  # Se o registro ainda não foi salvo
            # Encontra o maior ID específico do usuário atual e adiciona 1
            max_id = Auto.objects.filter(user=self.user).aggregate(models.Max('user_specific_id'))['user_specific_id__max']
            self.user_specific_id = 1 if max_id is None else max_id + 1
        super().save(*args, **kwargs)