from django.shortcuts import redirect, render 
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .forms import TODOForm
from .models import TODO
from django.core.mail import send_mail

def index(request):
#     send_mail(
#     "Testing_mail ",
#     "Thanks for connecting with us.",
#     "anurag504singh@gmail.com",
#     ["anuragsingh70718180+1@gmail.com"],
#     fail_silently=False,
# )

    form = TODOForm()
    if request.user.is_authenticated:
        todos = TODO.objects.filter(user=request.user).order_by('priority') 

         
    else:
        todos = TODO.objects.none()  
    return render(request, 'index.html', context={'form': form, 'todos': todos})
    
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2  = request.POST['password2']

        
        if password1 == password2 :
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username already taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email already exists')
                return redirect('register')
            else:
                user = User.objects.create_user(
                username = username , 
                first_name =first_name , 
                last_name =last_name , 
                password=password1 , 
                email = email)
                user.save()
                print('user_created')
                send_mail(
                    "Welcome to Our Website",  # Subject
                    f"Hello {first_name},\n\nThank you for registering on our website. \n\nYour Username : {username}",  # Message
                    "anurag504singh@gmail.com",  # From email (you need to configure this in settings)
                    [email],  # To email
                    fail_silently=False,  # You can set this to True if you want to suppress email sending errors
                )
            
                return redirect('login')
                
        else :
            messages.info(request,'Password not match')
            return redirect('register')
            

        
    else:
        return render(request,('register.html'))

 
    
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password  = request.POST['password']

        user = auth.authenticate(username = username , password = password)
        
        if user is not None :
            auth.login(request,user)
            return redirect("/")
            
        else:
            messages.info(request,'Invalid input')
            return redirect('login')


    else: 
        return render(request,'login.html')
    

def logout(request):
    auth.logout(request)
    return redirect("/")
    
def add(request):

    form = TODOForm(request.POST)
    if request.user.is_authenticated:
        user = request.user
        print(user)
        if form.is_valid():
            print(form.cleaned_data)
            todo = form.save(commit=False)
            todo.user =user
            todo.save()            
            
            
            return redirect("/")
        else:
            return render(request, 'index.html' , context={'form' : form}) 
        
def delete(request , id ):
    print(id)
    TODO.objects.get(pk = id ).delete()
    return redirect("/")

def change_status(request , id ,status):
    print(id)
    todo = TODO.objects.get(pk = id )
    todo.status = status
    todo.save()
    return redirect("/")

def edit_todo(request, id):
    todo = TODO.objects.get(pk=id)
    if request.method == 'POST':
        form = TODOForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = TODOForm(instance=todo)
    return render(request, 'edit_todo.html', {'form': form, 'todo': todo})






