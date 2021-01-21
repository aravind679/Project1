from django.shortcuts import render,redirect
from project.models import User,Sales
from django.http import HttpResponse
# Create your views here.

def home(request):
    return render (request,"home.html")

def about(request):
    return render(request,"about.html")

def login_user(request):
    if request.method=="POST":
        userid=request.POST["userid"]
        password=request.POST["password"]
        try:
            data = User.objects.get(pk=userid)
            if data.userid == userid and data.password == password:
                return redirect(f'/create/{userid}')
            else:
                return HttpResponse("Check ur password and try again")
        except:
            return HttpResponse("User does not exist!!!!")   
    return render(request,"login.html")

def signup_user(request):
    if request.method=="POST":
        userid=request.POST['userid']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        pnumber=request.POST['pnumber']
        try:
            data = User.objects.get(pk=userid)
            return redirect("/signup/")
        except:
            newdata=User.objects.create(userid=userid,username=username,email=email,password=password,pnumber=pnumber)
            return redirect(f'/create/{userid}')             
    return render (request,"signup.html")


def create(request,userid):
    d=User.objects.get(pk=userid)
    if request.method =="POST":
        amt=request.POST['amt']
        item=request.POST['item']
        quantity=request.POST['quantity']
        new_data=Sales(userid=d,amt=amt,item=item,quantity=quantity)
        new_data.save()
        return redirect(f"/mydata/{d.userid}")
    return render(request,"create.html",{'d':d})


def mydata(request,userid):
    mydata=Sales.objects.filter(userid=userid)
    return render(request,"mydata.html",{"my":mydata})


def view_data(request,dataid,userid):
    data=Sales.objects.get(pk=dataid)
    userdata=User.objects.get(pk=userid)
    return render (request,"data.html",{"choice":data, "userdata":userdata})

def delete_data(request,dataid,userid):
	data=Sales.objects.get(pk=dataid)
	data.delete()
	return redirect (f'/mydata/{userid}')

def edit_data (request,dataid,userid):
    data=Sales.objects.get(pk=dataid)
    if request.method =="POST":
        amt=request.POST['amt']
        item=request.POST['item']
        quantity=request.POST['quantity']
        data.amt=amt
        data.item=item
        data.quantity=quantity
        data.save()
        return redirect (f"/mydata/{userid}")
        
    return render (request,"edit.html",{"data":data})



