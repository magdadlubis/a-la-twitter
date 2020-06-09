from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView

from twitter.models import *
from twitter.forms import *


class MainPageView(LoginRequiredMixin, View):
    def get(self, request):
        form = AddTweetForm()
        tweets = Tweet.objects.all().order_by('-creation_date')
        return render(request, 'twitter/main_page.html', {'tweets': tweets, 'form': form})

    def post(self, request):
        form = AddTweetForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            user = self.request.user
            Tweet.objects.create(content=content, user=user)
            return redirect('/')
        return HttpResponse('Niepoprawne dane formularza!')


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'twitter/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                msg = 'Niepoprawny login lub hasło!'
                return render(request, 'twitter/login.html', {'form': form, 'msg': msg})
        #return render(request, 'twitter/login.html', {'form': form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect(reverse_lazy('main-page'))


class AddUserView(View):
    def get(self, request):
        form = AddUserForm()
        return render(request, 'twitter/add_user.html', {'form': form})

    def post(self, request):
        form = AddUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            if not UserModel.objects.filter(email=email):
                UserModel.objects.create_user(username=email, email=email, password=password)
                user = authenticate(username=email, password=password)
                if user is not None:
                    login(request, user)
                    return redirect(reverse_lazy('main-page'))
            else:
                msg = 'Nazwa użytkownika (e-mail) jest już w użyciu!'
                return render(request, 'twitter/add_user.html', {'form': form, 'msg': msg})
        #return render(request, 'twitter/add_user.html', {'form': form})

class UserView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(UserModel, pk=user_id)
        tweets = Tweet.objects.filter(user=user)
        return render(request, 'twitter/user.html', {'tweets': tweets, 'user': user})


class AddTweetView(LoginRequiredMixin, CreateView):
    model = Tweet
    fields = ['content']
    def form_valid(self, form):
        user = self.request.user
        content = form.cleaned_data.get('content')
        Tweet.objects.create(content=content, user=user)
        return redirect('/')


class TweetView(LoginRequiredMixin, View):
    def get(self, request, tweet_id):
        tweet = get_object_or_404(Tweet, pk=tweet_id)
        comments = Comment.objects.filter(tweet=tweet)
        form = CommentForm()
        print(tweet)
        print(comments)
        return render(request, 'twitter/tweet.html', {'tweet': tweet, 'comments': comments, 'form': form})

    def post(self, request, tweet_id):
        tweet = get_object_or_404(Tweet, pk=tweet_id)
        comments = Comment.objects.filter(tweet=tweet)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            Comment.objects.create(comment=comment, user=self.request.user, tweet=tweet)
            return redirect('tweet', tweet_id=tweet_id)
        return render(request, 'twitter/tweet.html', {'tweet': tweet, 'comments': comments, 'form': form})


class EditUserView(LoginRequiredMixin, View):
    def get(self, request):
        form = EditUserForm(instance=self.request.user)
        return render(request, 'twitter/edit_user.html', {'form': form})

    def post(self, request):
        form = EditUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            user = UserModel.objects.get(pk=self.request.user.pk)
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.set_password(password)
            user.save()
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('edit-user')
        return render(request, 'twitter/edit_user.html', {'form': form})


class MessagesView(LoginRequiredMixin, View):
    def get(self, request):
        received = Message.objects.filter(to=request.user).order_by('-date')
        sent = Message.objects.filter(sender=request.user).order_by('-date')
        return render(request, 'twitter/messages.html', {'received': received, 'sent': sent})


class MessageView(LoginRequiredMixin, View):
    def get(self, request, msg_id):
        message = Message.objects.get(pk=msg_id)
        if request.user == message.to:
            message.read = True
            message.save()
        return render(request, 'twitter/message.html', {'message': message})

class SendMessageView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        if user_id == request.user.pk:
            return HttpResponse('Nie możesz wysłać wiadomości do siebie')
        else:
            form = MessageForm()
            return render(request, 'twitter/send_message.html', {'form': form})

    def post(self, request, user_id):
        if user_id == request.user.pk:
            return HttpResponse('Nie możesz wysłać wiadomości do siebie')
        else:
            form = MessageForm(request.POST)
            if form.is_valid():
                message = form.cleaned_data['message']
                to = UserModel.objects.get(pk=user_id)
                Message.objects.create(message=message, to=to, sender=self.request.user)
            return redirect('messages')