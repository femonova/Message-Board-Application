from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Question, Comments, ExtraInfoForm, HasAlreadyVoted
from django.template import loader
from django.views import generic
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

# Create your views here.
#All Django wants is an HttpResponse

#@login_required(redirect_field_name='login')

#Usiing LoginRequiredMixin redirects you to that, but why doesnt it throw you back to reg since that's the redirect field name?
class IndexView(LoginRequiredMixin, generic.ListView):
    
    redirect_field_name = '/' #Does this take me to /polls/ (a.k. index???) OH! ITS THE WRONG PARAMETER! THE DEFAULT IS LOGIN  #login_url = '/login/'
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    paginate_by = 5

    def get_queryset(self):
        return Question.objects.all()

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    paginate_by = 2

    ####################################
    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs) 
        list_comments = self.object.comments_set.all()
        paginator = Paginator(list_comments, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            file_comments = paginator.page(page)
        except PageNotAnInteger:
            file_comments = paginator.page(1)
        except EmptyPage:
            file_comments = paginator.page(paginator.num_pages)

        context['list_comments'] = file_comments
        return context
    ######################################
class ResultsView(generic.DetailView):
    model = Question #What type of model we are working with
    template_name = 'polls/results.html' #template to be referenced

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

#This serves to interact with the database and redirect back to the current question
#I should really rename this
def vote(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    user_response = request.POST['usr_comment'] #Grab user comment
 
    if(user_response == ''):
        return render(request, 'polls/detail.html', {
        'question' : question,
        'error_message' : "No comment provided" #Prehaps restrict submission before sending post?
    })
    else: 
        question.comments_set.create(comment_text = user_response, upvotes = 0) #Associates question with comments
        return HttpResponseRedirect(reverse('polls:detail', args=(question_id, ))) 

def upvote_me(response, comment_id):

    current_user = response.user
    current_comment = Comments.objects.get(pk = comment_id)
 
    #return render(response, 'polls/detail/', {'question': Question.objects.get(pk = current_comment.question), 'error_message': 'Already upvoted this comment!'})
    has_voted = HasAlreadyVoted.objects.filter(user_id = current_user, comment_id = comment_id) #Apparently this just needs an integer

    #Checks to see if a specific (user, comment) pair exists or not. If not, add them to the db
    if(has_voted.count() == 0):
        #This needs the actual comment lazy object. Create entry and save it to db
        add_to_db = HasAlreadyVoted.objects.create(user_id = current_user, comment_id = current_comment) 
        add_to_db.save()

        #Count the user's upvote
        current_comment.upvotes += 1
        current_comment.save()
        return HttpResponseRedirect(reverse('polls:detail', args=(current_comment.question.id,)))
    else:
        return HttpResponseRedirect(reverse('polls:detail', args=(current_comment.question.id,)))


### Not sure if this is good practice or not, but I'll be adding user registration here ###
def reg_user(request):
    if(request.method == 'POST'):
        form = ExtraInfoForm(request.POST)
        if form.is_valid():
            user = form.save() #Apparently we dont need to auth because it has the user now?
            #username = form.cleaned_data.get('username')
            #password = form.cleaned_data.get('password')
            #user = authenticate(username = username, password = password)
            login(request, user)

            #will the bottom wotk
            return redirect ('/polls/')
    else:
        form = ExtraInfoForm()
    return render(request, 'registration/signup.html', {'form':form})

def user_submit_question(request):
    if(request.method == "POST"):
        new_question = Question(question_text = request.POST['usr_comment'], pub_date = timezone.now())
        new_question.save()
        return redirect ('/polls/')
    else:
        return render(request, '/polls/', {})

def log_me_out(request):
    if(request.method == "GET"):
        logout(request) #not request.user
        message = "Thanks for visiting! We hope to see you again!"
        return render(request, 'registration/logout.html', {'message': message})