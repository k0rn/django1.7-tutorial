from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.template import RequestContext,loader
from django.core.urlresolvers import reverse
from polls.models import Question,Choice
from django.views import generic
from django.utils import timezone

	
def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	template = loader.get_template('polls/index.html')
	context = RequestContext(request, {
	'latest_question_list': latest_question_list,})
	return HttpResponse(template.render(context))

# always comment previous definitions
#def index(request):
#	return HttpResponse("hello, polls index")
# Create your views here.

def detail(request, question_id):
	question = get_object_or_404(Question,pk=question_id)
	return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
	question = get_object_or_404(Question,pk=question_id)
	return render(request,'polls/results.html',{'question':question})


class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'
	
	def get_queryset(self):
		return Question.objects.filter(pub_date__lte = timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'
	
	def get_queryset(self):
		return Question.objects.filter(pub_date__lte = timezone.now())
	
class ResultView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'
	
	
def vote(request, question_id):
	p = get_object_or_404(Question,pk=question_id)
	try:
		selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except (KeyError,Choice.DoesNotExist):
		return render(request,'polls/detail.html',{
		'question':p,'error_message':"You didnt select a choice.",})
	else:
		selected_choice.votes +=1
		selected_choice.save()
		return HttpResponseRedirect(reverse('polls:results',args=(p.id)))
		
