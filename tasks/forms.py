from django import forms

from . import models


class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = (
            "title",
            'description',
            'status',
            'priority',
            'dude_date',
            'is_publick'
        )
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
        
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
    since = forms.DateTimeField(required=False, label='since')
    to = forms.DateTimeField(required=False, label='to')

class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['content','media']
        widgets  = {
            'content': forms.TextInput(),
            'media': forms.FileInput(),
        }