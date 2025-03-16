from django.db import models
from django.conf import settings
# Create your models here.

class UserFollowing(models.Model):
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='following', 
        on_delete=models.CASCADE
        )
    
    following_user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='followers', 
        on_delete=models.CASCADE
        )
    
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'following_user_id'], name='unique_followers')
        ]
        ordering = ['-created']

    def __str__(self):
        return f"{self.user_id} follows {self.following_user_id}"