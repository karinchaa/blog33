from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Tag(models.Model):
    tag = models.CharField(max_length=20, verbose_name='Тег')

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, default=1)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Автор')
    datetime = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время')
    text = models.TextField(max_length=200, verbose_name='Комментарий')

    def __str__(self):
        author_name = self.author.username if self.author else "Anonymous"
        return f'{author_name} - {self.datetime}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Коментарии'


class Post(models.Model):
    title = models.CharField(max_length=30, verbose_name='Оглавление')
    content = models.TextField(verbose_name='Описание')
    published_date = models.DateTimeField(auto_created=True, verbose_name='Дата и время')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    poster = models.ImageField(upload_to='post_images/', null=True, blank=True, verbose_name='Постер')
    tag = models.ManyToManyField(Tag, blank=True, related_name='posts', verbose_name='Тег')
    comments = models.ManyToManyField(Comment, blank=True, verbose_name="Комментарий", related_name='post_comments')

    def __str__(self):
        return self.user.username if self.user_id else "No User"

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.user.username


class Subscriber(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email