from django.db import models
import re
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
    super_tag = models.ForeignKey('self', null=True, blank=True, verbose_name='上级标签', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "标签"
        verbose_name_plural = verbose_name


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    grade = models.ForeignKey(Grade, blank=True, null=True, on_delete=models.CASCADE)
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', default=now)
    question_text = models.TextField()

    multiple_choice = 'MC'
    true_false = 'TF'
    essay = 'ES'
    fill_in_blank = 'FB'
    numeric_math = 'NM'

    TYPE_DICT = {
        multiple_choice: ('选择题', 'multiple-choice'),
        true_false: ('判断题', 'true-false'),
        essay: ('主观题', 'essay'),
        fill_in_blank: ('文字填空题', 'fill-in-blank'),
        numeric_math: ('数字填空题', 'numeric-math'),
    }

    TYPE_CHOICES = [
        (multiple_choice, '选择题'),
        (true_false, '判断题'),
        (essay, '主观题'),
        (fill_in_blank, '文字填空题'),
        (numeric_math, '数字填空题'),
    ]

    TYPE_SLUGS = [('选择题', 'multiple-choice'),
                  ('判断题', 'true-false'),
                  ('主观题', 'essay'),
                  ('文字填空题', 'fill-in-blank'),
                  ('数字填空题', 'numeric-math'),
                  ]

    type = models.CharField(
        '题型',
        max_length=2,
        choices=TYPE_CHOICES,
        default=essay,
    )

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    media_path = models.CharField(max_length=200, blank=True, null=True)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return str(self.subject) + ' ' + ', '.join([str(t) for t in self.tag.all()])

    special_char_list = [
        (r'\~', '~'),
        (r'\=', '='),
        (r'\#', '#'),
        (r'\{', '{'),
        (r'\}', '}')
    ]

    def answer(self):
        pat = re.compile(r'[^\\]\{(.*)[^\\]\}')
        ans = re.search(pat, self.question_text)
        return ans

    def escape_chars(self, s):
        for tup in self.special_char_list:
            s = re.sub(tup[0], tup[1], s)
        return s

    def restore_chars(self, s):
        for tup in self.special_char_list:
            s = re.sub(tup[1], tup[0], s)
        return s

    class Meta:
        ordering = ['id']
        verbose_name = "题目"
        verbose_name_plural = verbose_name
