import sys
from django.contrib import messages
from django.db.models.signals import post_save
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q
from django.contrib.auth.models import User
from will.models import AccountUser, Course, AttendingCourse
from will.signals import check_nim
from will.forms import StudentRegisterForm

# Create your views here.
def home(request):
    return render(request, 'home.html')

def readCourse(request):
    data = Course.objects.all()[:1]  # limit data (1 pcs)
    context = {'data_list': data}
    return render(request, 'course.html', context)

@csrf_protect
def createCourse(request):
    return render(request, 'home.html')

@csrf_protect
def updateCourse(request):
    return render(request, 'home.html')

@csrf_protect
def deleteCourse(request):
    try:
        data = Course.objects.filter(course_id=id)
        if user:
            data.delete()
            messages.success(request, 'Data Berhasil dihapus')
            return redirect('will:read-data-course')
        else:
            messages.success(request, 'Data Tidak ditemukan')
            return redirect('will:read-data-course')
    except:
        return redirect('will:read-data-course')

def readStudent(request):
    data = AccountUser.objects.all()
    context = {'data_list': data}
    return render(request, 'index.html', context)

@csrf_protect
def createStudent(request):
    if request.method == 'POST':
        forms = StudentRegisterForm(request.POST)
        if forms.is_valid():
            post_save.disconnect(check_nim)
            forms.fullname = forms.cleaned_data.get("fullname")
            forms.nim = forms.cleaned_data.get("nim")
            forms.email = forms.cleaned_data.get("email")
            post_save.send(
                sender=AccountUser,
                created=None,
                instance=forms,
                dispatch_uid="check_nim"
            )
            messages.success(request, 'Data Berhasil disimpan')
            return redirect('will:read-data-student')
    else:
        forms = StudentRegisterForm()
    return render(request, 'form.html', {'forms': forms})

@csrf_protect
def updateStudent(request, id):
    forms_update = AccountUser.objects.get(account_user_related_user=id)
    if request.method == 'POST':
        forms = StudentRegisterForm(request.POST)
        if forms.is_valid():
            forms_update.account_user_fullname = forms.cleaned_data.get("fullname")
            forms_update.account_user_student_number = forms.cleaned_data.get("nim")
            forms_update.account_user_related_user = forms.cleaned_data.get("email")
            forms_update.account_user_updated_by = request.user.username
            forms_update.save()
            messages.success(request, 'Data Berhasil diupdate')
            return redirect('will:read-data-student')
    else:
        forms = StudentRegisterForm(initial={
            'fullname': forms_update.account_user_fullname,
            'nim': forms_update.account_user_student_number,
            'email': forms_update.account_user_related_user,
        })
    return render(request, 'form.html', {'forms': forms})

@csrf_protect
def deleteStudent(request, id):
    member = AccountUser.objects.get(account_user_related_user=id)
    user = User.objects.get(username=id)
    member.delete()
    user.delete()
    messages.success(request, 'Data Berhasil dihapus')
    return redirect('will:read-data-student')