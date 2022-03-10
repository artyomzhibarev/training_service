from django.contrib import admin
from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import (Topic, Answer, Question, TrainingTest, TrainingTestCustomerRelation, TrainingTestTaker)


class InlineFormset(BaseInlineFormSet):

    def clean(self):
        super().clean()
        if not any(item.get('is_correct') for item in self.cleaned_data):
            raise ValidationError(_('The question must have at least one correct answer.'))


class AnswerInline(admin.TabularInline):
    model = Answer
    fields = ('answer_text', 'id', 'is_correct', 'comment_correct', 'comment_incorrect')
    formset = InlineFormset
    extra = 0


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer_text', 'id', 'is_correct', 'created_at')
    list_filter = ('question', 'question__training_test')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'id', 'training_test', 'created_at')
    inlines = (AnswerInline,)
    list_filter = ('training_test', )


@admin.register(TrainingTest)
class TrainingTestAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(TrainingTestCustomerRelation)
class TrainingTestCustomerRelationAdmin(admin.ModelAdmin):
    ...


@admin.register(TrainingTestTaker)
class TrainingTestTakerAdmin(admin.ModelAdmin):
    list_display = ('customer', 'id', 'training_test', 'score', 'completed', 'date_finished')
