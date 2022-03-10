from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=100)
    content_text = models.TextField()

    def __str__(self):
        return self.name


class Answer(models.Model):
    answer_text = models.CharField(max_length=200)
    question = models.ForeignKey('Question', related_name='answers', on_delete=models.DO_NOTHING)
    is_correct = models.BooleanField(default=False)
    comment_correct = models.CharField(max_length=200)
    comment_incorrect = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.answer_text


class Question(models.Model):
    question_text = models.TextField(unique=True)
    training_test = models.ForeignKey('TrainingTest', related_name='questions', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text


class TrainingTest(models.Model):
    name = models.CharField(max_length=100)
    topic = models.ForeignKey(Topic, on_delete=models.DO_NOTHING, related_name='tests')
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()

    def __str__(self):
        return f'{self.name}: {self.topic.name}'


class TrainingTestTaker(models.Model):
    customer = models.ForeignKey('users.Customer', on_delete=models.CASCADE)
    training_test = models.ForeignKey(TrainingTest, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    date_finished = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.customer}: {self.training_test.name}: {self.score}: {self.completed}'


class TrainingTestCustomerRelation(models.Model):
    customer = models.ForeignKey(TrainingTestTaker, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Test result'
        verbose_name_plural = 'Test results'

    def __str__(self):
        return f'{self.customer}: {self.question.question_text}: {self.answer}'
