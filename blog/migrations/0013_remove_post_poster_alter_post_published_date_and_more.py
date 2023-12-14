# Generated by Django 4.2.7 on 2023-12-13 13:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_subscriber'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='poster',
        ),
        migrations.AlterField(
            model_name='post',
            name='published_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата и время'),
        ),
        migrations.CreateModel(
            name='PostImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='post_images/', verbose_name='Изображение')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='blog.post', verbose_name='Пост')),
            ],
        ),
    ]