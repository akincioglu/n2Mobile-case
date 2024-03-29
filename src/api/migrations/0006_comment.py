# Generated by Django 4.2.9 on 2024-02-02 20:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_rename_user_album_userid_rename_user_post_userid_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('body', models.TextField()),
                ('postId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.post')),
            ],
        ),
    ]
