# Generated by Django 4.1.1 on 2022-11-08 09:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Main_Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_category_name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('thumbnail', models.ImageField(blank=True, upload_to='photos/thumbanil')),
            ],
        ),
        migrations.CreateModel(
            name='Sub_Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_cat_name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('parent_main', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.main_category')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=300, unique=True)),
                ('slug', models.SlugField(default='', max_length=300, null=True, unique=True)),
                ('prdt_desc', models.TextField(null=True)),
                ('price', models.IntegerField()),
                ('images', models.ImageField(upload_to='product/images')),
                ('img1', models.ImageField(blank=True, upload_to='product/images')),
                ('img2', models.ImageField(blank=True, upload_to='product/images')),
                ('img3', models.ImageField(blank=True, upload_to='product/images')),
                ('stock', models.IntegerField(null=True)),
                ('is_available', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now_add=True)),
                ('parent_main_prdt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.main_category')),
                ('parent_sub_prdt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.sub_category')),
            ],
        ),
    ]
