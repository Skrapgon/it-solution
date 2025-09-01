from django.db import models
from django.contrib.auth.models import User

class Quote(models.Model):
    SOURCE_TYPES = [
        ('book', 'Книга'),
        ('movie', 'Фильм'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quotes')
    text = models.TextField('Текст цитаты')
    source = models.CharField('Произведение', max_length=255)
    source_type = models.CharField('Тип произведения', choices=SOURCE_TYPES, max_length=10)
    priority = models.IntegerField('Приоритет', default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    likes = models.ManyToManyField(User, related_name='liked_quotes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_quotes', blank=True)
    views = models.IntegerField('Число просмотров', default=0)

    def __str__(self):
        return f'{self.text[:50]}... ({self.user.username})'

    def can_add_quote(user, text, source, source_type):
        if Quote.objects.filter(user=user, source=source, source_type=source_type, text=text).exists():
            return False
        return Quote.objects.filter(source=source, source_type=source_type).count() < 3
    
    @staticmethod
    def get_top_n_by_likes(n):
        return Quote.objects.annotate(likes_count=models.Count('likes')).order_by('-likes_count')[:n]
        