from django import template
from django.template.loader import render_to_string

register = template.Library()

@register.simple_tag
def render_special(special):
    return render_to_string('special_template.html', {'special': special})