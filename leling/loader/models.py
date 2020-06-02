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
    multiple_answer = 'MA'

    TYPE_DICT = {
        multiple_choice: ('选择题', 'multiple-choice'),
        true_false: ('判断题', 'true-false'),
        essay: ('主观题', 'essay'),
        fill_in_blank: ('文字填空题', 'fill-in-blank'),
        numeric_math: ('数字填空题', 'numeric-math'),
        multiple_answer: ('多选题', 'multiple-answer'),
    }

    TYPE_CHOICES = [
        (multiple_choice, '选择题'),
        (true_false, '判断题'),
        (essay, '主观题'),
        (fill_in_blank, '文字填空题'),
        (numeric_math, '数字填空题'),
        (multiple_answer, '多选题'),
    ]

    TYPE_SLUGS = [('选择题', 'multiple-choice'),
                  ('判断题', 'true-false'),
                  ('主观题', 'essay'),
                  ('文字填空题', 'fill-in-blank'),
                  ('数字填空题', 'numeric-math'),
                  ('多选题', 'multiple-answer'),
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
        (r'\\~', '~'),
        (r'\\=', '='),
        (r'\\#', '#'),
        (r'\\{', '{'),
        (r'\\}', '}')
    ]

    ANSWER_PATTEN = re.compile(r'(?<!\\)({(?:.|\s)*?(?<!\\)})')

    def answer(self):
        ans = re.findall(self.ANSWER_PATTEN, self.question_text)
        return ans

    # return
    # rubrics = [
    #   ['NM', (False, (0,2), 50, ''), (True, (1,1), 100, '')],
    #   ['MC', (False, 'A', -50, ''), (False, 'B', 50, 'Right'), (False, 'C', 50, 'Right')]
    #   ]
    def rubric(self):
        answers = self.answer()
        rubrics = []
        for ans in answers:
            ans = ans[1:-1]
            is_numeric = False
            if re.match('#', ans):
                is_numeric = True
                ans = ans[1:]
            rub = [is_numeric]
            choices = re.findall(r'(?:~|=)[^~=]*', ans)
            if len(choices) == 0:
                choices.append(ans)
            for choice in choices:
                try:
                    comment = restore_chars(re.search(r'#((?:.|\s)*)', choice).group(1))
                    choice = re.sub(r'#((?:.|\s)*)', '', choice)
                except:
                    comment = ''
                score = 0
                if re.match('~', choice):
                    is_correct = False
                    choice = choice[1:]
                elif re.match('=', choice):
                    is_correct = True
                    score = 100
                    choice = choice[1:]
                else:
                    is_correct = True
                    score = 100
                choice = re.sub(r'\s*$', '', choice)
                try:
                    match = re.search(r'%(-?(?:[1-9]?[0-9]|100))%(.*)', choice)
                    score = int(match.group(1))
                    choice = match.group(2)
                except:
                    pass
                option = restore_chars(choice)
                if is_numeric:
                    interval = re.search(r'(\d+(?:\.\d)?\d*)\.\.(\d+(?:\.\d)?\d*)', option)
                    if interval is None:
                        interval = re.search(r'(\d+(?:\.\d)?\d*):(\d+(?:\.\d)?\d*)', option)
                        mean = float(interval.group(1))
                        delta = float(interval.group(2))
                        option = (mean-delta, mean+delta)
                    else:
                        option = (float(interval.group(1)), float(interval.group(2)))

                rub.append((is_correct, option, score, comment))
            rubrics.append(rub)
        return rubrics

    # ans_list = [(1.1),('A', 'B')]
    # rubrics = [
    #   ['NM', (False, (0,2), 50, ''), (True, (1,1), 100, '')],
    #   ['MC', (False, 'A', -50, ''), (False, 'B', 50, 'Right'), (False, 'C', 50, 'Right')]
    #   ]
    # return = [(100, [(1, '')]), (0, [('A', ''), ('B', 'Right)])]
    def grade_answer(self, ans_list):
        rubrics = self.rubric()
        if len(rubrics) == 0:
            raise
        if len(ans_list) != len(rubrics):
            raise Exception
        result = []
        for i in range(len(ans_list)):
            ans = ans_list[i]
            rub = rubrics[i]
            comments = []
            score = 0
            is_numeric = rub[0]
            for r in rub[1:]:
                sample = r[1]
                rubric_score = r[2]
                if is_numeric:
                    num = ans[0]
                    if sample[0] <= num <= sample[1] and rubric_score > score:
                        score = rubric_score
                        comment = (num, r[3])
                        comments.append(comment)
                else:
                    for a in ans:
                        if a == sample:
                            score += rubric_score
                            comment = (a, r[3])
                            comments.append(comment)

                score = min(100, score)
                score = max(0, score)
                result.append((score, comments))

        return result

    def stem(self):
        underline = '__________'
        stem = re.sub(self.ANSWER_PATTEN, underline, self.question_text)
        stem = restore_chars(stem)
        stem = re.sub(underline + '$', '', stem)
        return stem



    class Meta:
        ordering = ['id']
        verbose_name = "题目"
        verbose_name_plural = verbose_name


def escape_chars(s):
    for tup in Question.special_char_list:
        s = re.sub(tup[1], tup[0], s)
    return s


def restore_chars(s):
    for tup in Question.special_char_list:
        s = re.sub(tup[0], tup[1], s)
    return s