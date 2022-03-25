from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Enrollment
from .forms import ContactCourse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

# Create your views here.
def list(request):
    courses = Course.objects.all()
    template_name = "list.html"
    context = {
        'courses' : courses
    }
    return render(request, template_name, context)

def detail_pk(request, pk):
    course = get_object_or_404(Course, pk=pk)
    context = {
        'course' : course,
    }
    if request.method == 'POST':
        form = ContactCourse(request.POST)
        if form.is_valid():
            context['is_valid'] = True
            form.send_mail(course)
            form = ContactCourse()
    else:
        form = ContactCourse()

    context['formContact'] = form
    template_name = "detail.html"
    return render(request, template_name, context)

def detail_slug(request, slug):
    course = get_object_or_404(Course, slug=slug)
    context = {
        'course' : course
    }
    if request.method == 'POST':
        form = ContactCourse(request.POST)
        if form.is_valid():
            context['is_valid'] = True
            form.send_mail(course)
            form = ContactCourse()
    else:
        form = ContactCourse()
    context['formContact'] = form
    template_name = "detail.html"
    return render(request, template_name, context)

def enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if not request.user.is_authenticated:
        return redirect('panel:login')
    
    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user,course=course
    )

    if created:
        #enrollment.active()
        messages.success(request, 'Sua inscrição foi realizada com sucesso!')
    else:
        messages.info(request, 'Vocé já possui inscrição no curso')
    
    return redirect('panel:dashboard')
