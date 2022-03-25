from django.template import Library
from courses.models import Enrollment
register = Library()

@register.inclusion_tag('tags/my_courses.html')
def my_courses(user):
    enrollments = Enrollment.objects.filter(user=user)
    context ={
        'enrollments': enrollments
    }
    return context

