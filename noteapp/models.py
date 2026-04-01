from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class Document(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Document'
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'

    def __str__(self):
        return self.title
    
class DocumentAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('user', 'document')
        db_table = 'DocumentAccess'
        verbose_name = 'Document Access'
        verbose_name_plural = 'Document Access'

    def __str__(self):
        return f'{self.document.title}' + '  ' + f'{self.user.username}'  
    