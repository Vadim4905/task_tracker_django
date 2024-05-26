from django import forms
from django.contrib.admin.widgets import   AdminDateWidget, AdminTimeWidget,AdminSplitDateTime

from . import models


class TaskForm(forms.ModelForm):
    due_date = forms.SplitDateTimeField(
        widget=AdminSplitDateTime,
        required=False,
        label = 'due date'
    )
    
    class Meta:
        model = models.Task
        fields = (
            "title",
            'description',
            'status',
            'priority',
            'due_date',
            'is_publick'
        )
        widgets ={
            "due_date" :AdminDateWidget,
        }

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            pass
            # self.fields[field].widget.attrs.update({"class": "form-control"})
        
class TaskFilterForm(forms.Form):
    STATUS_CHOICES=[
        ('','All'),
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done' ,'Done'),
    ]
    PRIORITY_CHOICES=[
            ('','All'),
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'HIgh'),
            ('critical', 'Critical'),
        ]
        
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False, label='status')
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES, required=False, label='priority')
    since = forms.SplitDateTimeField(
        widget=AdminSplitDateTime,
        required=False,
        label = 'since deadline'
    )
    to = forms.SplitDateTimeField(
        widget=AdminSplitDateTime,
        required=False,
        label = 'to dealine'
    )

class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['content','media']
        widgets  = {
            'content': forms.TextInput(),
            'media': forms.FileInput(),
        }