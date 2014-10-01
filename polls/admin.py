from django.contrib import admin
from polls.models import Question
from polls.models import Choice,Question

class QuestionAdmin(admin.ModelAdmin):
	fieldsets = [(None,{'fields':['question_text']}),('Date information',{'fields':['pub_date']})]
	list_display=('question_text','pub_date','was_published_recently')
	list_filter = ['pub_date']
	search_fields=['question_text']
admin.site.register(Question)
admin.site.register(Choice)


class ChoiceInline(admin.TabularInline):
	model = Choice
	extra = 3

# Register your models here.
