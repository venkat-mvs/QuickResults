from django.shortcuts import render,redirect
from django.template.loader import render_to_string

from django.contrib.auth import logout
from django.http import HttpResponse,HttpResponseForbidden,HttpResponseNotFound,HttpResponseRedirect

from .models import StudentsList
from .forms import StudentAddForm
from django.core.mail import EmailMultiAlternatives
# Create your views here.


from engine import webscrap
from engine import mailer


def send_to(request,id):
    if not request.user.is_superuser:
        return HttpResponseForbidden('admin only performs action')
    
    try:
        student = StudentsList.objects.get(studentid=id)
    except Exception as e:
        return HttpResponseNotFound(str(e))
    if student.mail_sent:
        return HttpResponse("ok")
    
    url = "http://www.nriitexamcell.com/autonomous/results/2-1-nov-2019.php"
    obj = webscrap.MarksWebScraper(url)
    
    id = student.studentid
    stu_mail = student.email_address
    form = {"roll":id,"submit":"Submit"}
    
    results = obj.get_results(form)
    if results == None:
        return HttpResponseNotFound("Wrong registration number")
    results["name"] = student.name
    
    rendered_text = render_to_string('results_template_text.html',context=results)
    rendered_html = render_to_string('results_template_html.html',context=results)
    msg = EmailMultiAlternatives(
        'Quick Results',
        rendered_text,
        to = [stu_mail]
    )
    msg.attach_alternative(rendered_html,'text/html')
    try:
        msg.send()
        student.mail_sent = True
        student.save()
    except:
        student.mail_sent = False
        student.save()
    
    return HttpResponse("ok")

def login(request):
    if request.user.is_authenticated:
        return redirect('home')
 
def reset(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        for student in StudentsList.objects.all():
            student.mail_sent = False
            student.save()
        return redirect('home')
  
def logout_admin(request):
    if  request.user.is_authenticated:
        logout(request)    
    return redirect('login')  

def edit_student(request,id):
    if request.method == 'POST':
        form =  StudentAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        student = StudentsList.objects.filter(studentid=id)[0]
        form = StudentAddForm()
        form.student_id = student.studentid
        form.name = student.name
        form.email_address = student.email_address
        form.mail_sent = student.mail_sent
        
    return render(request,'add_student.html',{'form':form})

def add_student(request):
    if request.method == 'POST':
        form =  StudentAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = StudentAddForm()
    return render(request,'add_student.html',{'form':form})

def student_list(request):
    if not request.user.is_authenticated:
        return redirect("login")
    
    return render(request,'student_list.html',context={'students':StudentsList.objects.all()})