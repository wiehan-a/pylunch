from django import template
from django.template.loader import render_to_string

register = template.Library()

@register.simple_tag
def render_special_price(special):
    return render_to_string('special_price_template.html', 
                                {'special': special})

@register.simple_tag
def render_special_supermini(special):
    return render_to_string('special_template_supermini.html', 
                                {'special': special})

@register.simple_tag
def render_special_mini(special):
    return render_to_string('special_template_mini.html', 
                                {'special': special})

@register.simple_tag
def render_special_full(special):
    return render_to_string('special_template_full.html', 
                                {'special': special})

@register.simple_tag
def render_restaurant_mini(restaurant):
    return render_to_string('restaurant_template_mini.html', 
                                {'restaurant': restaurant})

@register.simple_tag
def render_restaurant_full(restaurant):
    return render_to_string('restaurant_template_mini.html', 
                                {'restaurant': restaurant})

@register.simple_tag
def render_map_preamble(location):
    return render_to_string('map_preamble_template.html', 
                                {'location': location})