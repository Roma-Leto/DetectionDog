from  django import template
import marathon.views as views


register = template.Library()

@register.simple_tag()
def get_same():
    pass