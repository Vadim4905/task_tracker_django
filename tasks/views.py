from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView,DetailView,CreateView,View,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied ,ViewDoesNotExist
from django.utils import timezone

from . import mixins
from . import models
from . import forms

# Create your views here.



class TaskListView(ListView):
    model =models.Task
    context_object_name = 'tasks'
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(is_publick=True)
        if self.request.user.is_authenticated:
            queryset = queryset | self.request.user.tasks.filter(is_publick=False)
            # queryset = queryset.union(self.request.user.tasks.filter(is_publick=False))
            
        status = self.request.GET.get('status','')
        priority = self.request.GET.get('priority','')
        since = self.request.GET.get('since','')
        to = self.request.GET.get('to','')
        if status:
            queryset = queryset.filter(status=status)
        if priority:
            queryset = queryset.filter(priority=priority)
        if since:
            queryset = queryset.filter(due_date__gte=since)
        if to:
            queryset = queryset.filter(due_date__lte=to)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = forms.TaskFilterForm(self.request.GET)
        context['task_form'] = forms.TaskForm(self.request.GET)
        return context
    

        
class TaskFilterView(TaskListView):
    def get_queryset(self):
        queryset = super().get_queryset()
        now = timezone.now()
        if self.kwargs.get('category') == 'no-due-date':
            queryset = queryset.filter(due_date=None)
        if self.kwargs.get('category') == 'missing':
            queryset = queryset.filter(due_date__lte=now)
        if self.kwargs.get('category') == 'assigned':
            queryset = queryset.filter(due_date__gte=now)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get('category') == 'no-due-date':
            context['no-due-date'] = 'active'
        if self.kwargs.get('category') == 'missing':
            context['missing'] = 'active'
        if self.kwargs.get('category') == 'assigned':
            context['assigned'] = 'active'
        return context
    
    
class TaskDetailView(LoginRequiredMixin,DetailView):
    model = models.Task
    context_object_name = 'task'
    
    def dispatch(self,request,*args,**kwargs):
        instance =self.get_object()
        if instance.creator != self.request.user and instance.is_publick == False:
            raise ViewDoesNotExist
        return super().dispatch(request,*args,**kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = forms.CommentForm() 
        return context

    def post(self, request, *args, **kwargs):
        comment_form = forms.CommentForm(request.POST,request.FILES)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.creator = request.user
            comment.task = self.get_object()
            comment.save()
            return redirect('tasks:task-detail', pk=comment.task.pk)
        else:
            # Тут можна обробити випадок з невалідною формою
            pass
        
    
class TaskCreateView(LoginRequiredMixin,CreateView):
    model = models.Task
    form_class = forms.TaskForm
    success_url = reverse_lazy('tasks:task-list')

    def form_valid(self,form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
    
class TaskCompleteView(LoginRequiredMixin,mixins.UserIsOwner,View):
    def post(self,request,*args,**kwargs):
        task = self.get_object()
        task.status= 'done'
        task.save()
        return  HttpResponseRedirect(reverse_lazy('tasks:task-list'))
    
    def get_object(self):
        task_id =self.kwargs.get('pk')
        return get_object_or_404(models.Task,pk=task_id)
    

class TaskUpdateView(LoginRequiredMixin,mixins.UserIsOwner,UpdateView):
    model = models.Task
    form_class= forms.TaskForm
    success_url = reverse_lazy('tasks:task-list')

class TaskDeleteView(LoginRequiredMixin,mixins.UserIsOwner,DeleteView):
    model = models.Task
    success_url = reverse_lazy('tasks:task-list')
    


class CommentUpdateView(LoginRequiredMixin,mixins.UserIsOwner,UpdateView):
    model = models.Comment
    form_class= forms.CommentForm
    # success_url = reverse_lazy('tasks:task-list')
    
    def get_success_url(self):
        return reverse_lazy('tasks:task-detail', kwargs={'pk': self.object.task.pk})

class CommentDeleteView(LoginRequiredMixin,mixins.UserIsOwner,DeleteView):
    model = models.Comment
    # success_url = reverse_lazy('tasks:task-list')
    
    def get_success_url(self):
        return reverse_lazy('tasks:task-detail', kwargs={'pk': self.object.task.pk})
    
    
class CommentLikeToggle(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(models.Comment, pk=self.kwargs.get('pk'))
        like_qs = models.Like.objects.filter(comment=comment, user=request.user)
        if like_qs.exists():
            like_qs.delete()
        else:
            models.Like.objects.create(comment=comment, user=request.user)
        return redirect('tasks:task-detail', pk=comment.task.pk)