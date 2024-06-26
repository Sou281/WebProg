import sys
from django.contrib import messages
from django.db.models.signals import post_save
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q
from django.contrib.auth.models import User
from will.models import AccountUser
from will.signals import check_nim
from will.forms import StudentRegisterForm


# Create your views here.
def readStudent(request):
    data = AccountUser.objects.all()

    context = {'data_list': data}

    return render(request, 'index.html', context)


@csrf_protect
def createStudent(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            post_save.disconnect(check_nim)
            form.fullname = form.cleaned_data.get("fullname")
            form.nim = form.cleaned_data.get("nim")
            form.email = form.cleaned_data.get("email")
            post_save.send(
                sender=AccountUser, created=None,                
                instance=form,                
                dispatch_uid="check_nim")
            messages.success(request, 'Data Berhasil disimpan')
            return redirect('will:read-data-student')
    else:
        form = StudentRegisterForm()

    return render(request, 'form.html', {'form': form})


@csrf_protect
def updateStudent(request, id):
    #Create Your Task Here...    messages.success(request, 'Data Berhasil disimpan')
    return redirect('will:read-data-student')


@csrf_protect
def deleteStudent(request, id):
    member = AccountUser.objects.get(account_user_related_user=id)
    user = User.objects.get(username=id)
    member.delete()
    user.delete()
    messages.success(request, 'Data Berhasil dihapus')
    return redirect('will:read-data-student')