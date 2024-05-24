from django import template

register = template.Library()

@register.filter(name="endswith")
def endswith(value,arg):
    return value.lower().endswith(arg.lower()) 

@register.filter(name="intersection")
def endswith(list1,list2):
    return set(list1).intersection(set(list2))