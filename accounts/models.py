from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # 将来的にカスタムフィールドを追加する場合はここに記述
    
    def __str__(self):
        return self.username
