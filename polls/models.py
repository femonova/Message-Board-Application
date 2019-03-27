import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms
from django.conf import settings


# Create your models here.
#Each model has number of class variables that rep a database field
#Fields: IntegerField for ints, CharField for Char, etc.

class ExtraInfoForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.CharField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', )
    def updated_save(self):
        user = super(ExtraInfoForm, self).save() #I think of it as saving all the other info first before outr extensions (super calls the super version!)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()
        return User


class Question(models.Model):
    #Question text, pub date would be database column names
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published') #date published as human readable name (optional first positional arguement (doubles as documentatiton)
    def __str__(self): #Important when trying to represent object
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
        
class Comments(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    poster_name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default= 1)
    comment_text = models.CharField(max_length=200)
    upvotes = models.IntegerField(default=0)

    def __str__(self):
        return self.comment_text

class HasAlreadyVoted(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default = 0)
    comment_id = models.ForeignKey(Comments, on_delete=models.CASCADE)

    def __str__(self):
        constructed_string = 'User: ' + self.user_id + ' :Comment: '  + self.comment_id
        return constructed_string
    
    def did_user_vote(self, user_id):
        return self.user_id == user_id #Assuming it is stored as an integer

    
