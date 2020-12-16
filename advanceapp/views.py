from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .forms import UserRegisterForm,UserUpdate,ProfileUpdate
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from advanceapp.models import shorturl
from advanceapp.models import UserDetail
import random,string
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse
# Create your views here.
@login_required(login_url="userlogin")
def profile(request):
    if request.method=='POST':
        u_form=UserUpdate(request.POST,instance=request.user)
        p_form=ProfileUpdate(request.POST,request.FILES,instance=request.user.userdetail)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
    else:
       u_form=UserUpdate(instance=request.user)
       p_form=ProfileUpdate(instance=request.user.userdetail)
    return render(request,'profile.html',{'u_form':u_form,'p_form':p_form})

@login_required(login_url="userlogin")
def changepass(request):
    if request.method=="POST":
        form=PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
           v=form.save()
           update_session_auth_hash(request,v)
           return HttpResponse("Password Changed !")
    else:
        form=PasswordChangeForm(request.user)
    params={
        'form':form,
    }
    return render(request,'changepass.html',{'form':form})
def home(request,query=None):
    if not query or query is None:
       return render(request,'home.html')
    else:
       try:
           check=shorturl.objects.get(short_query=query)
           check.visits=check.visits+1
           check.save()
           url_to_redirect=check.original_url
           return redirect(url_to_redirect)
       except shorturl.DoesNotExist:
           return render(request,'home.html',{'error':"error"})
@login_required(login_url="userlogin")
def dashboard(request):
    usr=request.user
    urls=shorturl.objects.filter(user=usr)
    return render(request,'dashboard.html',{'urls':urls})

def randomgen():
    return''.join(random.choice(string.ascii_lowercase) for _ in range(6))

@login_required(login_url="userlogin")
def deleteurl(request):
    if request.method=="POST":
        short=request.POST['delete']
        try:
            check=shorturl.objects.filter(short_query=short)
            check.delete()
            return redirect(dashboard)
        except shorturl.DoesNotExist:
            return redirect(home)

    else:
        return redirect(home)

@login_required(login_url="userlogin")
def generate(request):
    if request.method=="POST":
        #generate
        pass
        if request.POST['original'] and request.POST['short']:
            #generate based on user input
            usr=request.user
            original=request.POST['original']
            short=request.POST['short']
            check=shorturl.objects.filter(short_query=short)
            if not check:
                newurl=shorturl(user=usr,original_url=original,short_query=short)
                newurl.save()
                return redirect(dashboard)
            else:
                messages.error(request,"Already Exists")
                return redirect(dashboard)
        elif request.POST['original']:
            #generate randomly
            usr=request.user
            original=request.POST['original']
            generated=False
            while not generated:
                short=randomgen()
                check=shorturl.objects.filter(short_query=short)
                if not check:
                    newurl=shorturl(user=usr,original_url=original,short_query=short)
                    newurl.save()
                    return redirect(dashboard)
                else:
                    continue

        else:
            messages.error(request,"Empty Fields")
            return redirect(dashboard)


    else:
        return redirect(dashboard)

def userlogin(request):
     if not request.user.is_authenticated:
         if request.method=="POST":
             if request.POST['email'] and request.POST['password']:
                email=request.POST['email']
                password=request.POST['password']
                username=User.objects.get(email=email.lower()).username
                user=authenticate(request,username=username,password=password)
                if user:
                   auth.login(request,user)

                   if request.POST['next']!='':
                      return redirect(request.POST.get('next'))
                   else:
                      return redirect(home)
                   return redirect(home)
                else:
                   return render(request,'login.html',{'error':"User Doesnt Exist"})
             else:
                 return render(request,'login.html',{'error':"Empty Fields"})
         else:
             return render(request,'login.html')
     else:
        return redirect(home)



def signup(request):
    if request.method=='POST':
         form=UserRegisterForm(request.POST)
         if form.is_valid():
             mob=form.cleaned_data.get('mobile')
             username=form.cleaned_data.get('username')
             form.save()
             UserDetail(user=User.objects.filter(username=username).first(),mobile=mob).save()
    else:
          form=UserRegisterForm()
          return render(request,'signup.html',{'form':form})

def userlogout(request):
    auth.logout(request)
    return redirect(userlogin)
