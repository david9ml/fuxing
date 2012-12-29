from django import template
register = template.Library()

@register.filter(name='cut_cn')
def cut_cn(value):
    print "TTTTTTTTTTTTTTTTTTTTT"+str(len(value))
    print "!!!!!!!!!!!!!!!!!!!"
    return value.replace('cn', '')
