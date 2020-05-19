from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils.timezone import now


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', default=now)
    question_text = models.CharField(max_length=200)
    
    class Meta:
        ordering = ['id']
        verbose_name = "题目"
        verbose_name_plural = verbose_name


class Tag(models.Model):
    """文章标签"""
    name = models.CharField('标签名', max_length=30, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "标签"
        verbose_name_plural = verbose_name


class Subject(models.Model):

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "学科"
        verbose_name_plural = verbose_name
