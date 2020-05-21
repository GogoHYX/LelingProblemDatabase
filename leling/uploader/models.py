from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils.timezone import now


class Subject(models.Model):
    name = models.CharField('学科名', max_length=5, primary_key=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "学科"
        verbose_name_plural = verbose_name


class Grade(models.Model):
    name = models.CharField('年级名', max_length=5, primary_key=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "年级"
        verbose_name_plural = verbose_name


class Tag(models.Model):
    """文章标签"""
    name = models.CharField('标签名', max_length=30, primary_key=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, blank=True, null=True, on_delete=models.CASCADE)
    super_tag = models.ForeignKey('self', null=True, blank=True, verbose_name='上级标签', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "标签"
        verbose_name_plural = verbose_name


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', default=now)
    question_text = models.TextField()
    subject = models.ForeignKey(Subject, on_delete='Cascade')
    rubric = models.TextField()
    media_path = models.CharField(max_length=200)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return str(self.subject) + ' ' + ', '.join([str(t) for t in self.tag_set.all()])

    class Meta:
        ordering = ['id']
        verbose_name = "题目"
        verbose_name_plural = verbose_name


