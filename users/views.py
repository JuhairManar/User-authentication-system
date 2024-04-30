from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import RegisterForm,ChangeUserData
#RegisterForm #for user registration 
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm,SetPasswordForm
#PasswordResetForm needs old password for new password
#SetPassWordForm doesn't need old password
#django.contrib.auth.forms has all the authentication related
#AuthenticationForm has user name and pass
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
#update_session_auth_hash to hash the pass

def home(request):
    return render(request,"home.html")

def signup(request):
    return render(request,'signup_types.html')

def doctor_signup(request):
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()  
            
            if 'profile_picture' in request.FILES:
                user.profile_picture = request.FILES['profile_picture']
                user.save()  
            
            messages.success(request, 'Doctor Account Created Successfully')
            
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                messages.error(request, 'Failed to authenticate user.')
                
                return redirect('login')  
        else:
            messages.error(request, 'Form validation failed.')
    else:
        form = RegisterForm()
    
    return render(request, "signup.html", {'form': form})


def patient_signup(request):
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()  
            
            if 'profile_picture' in request.FILES:
                user.profile_picture = request.FILES['profile_picture']
                user.save()  
            
            messages.success(request, 'Patient Account Created Successfully')
            
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                messages.error(request, 'Failed to authenticate user.')
                
                return redirect('login')  
        else:
            messages.error(request, 'Form validation failed.')
    else:
        form = RegisterForm()
    
    return render(request, "signup.html", {'form': form})

def login_page(request):
    return render(request,'login_types.html')

def user_login(request):
    if request.user.is_authenticated: #already logged in
        return redirect('profile')
    if request.method=='POST':
        form=AuthenticationForm(request=request,data=request.POST)
        if form.is_valid():
            name=form.cleaned_data['username']
            user_pass=form.cleaned_data['password']
            user=authenticate(username=name,password=user_pass) #checking if user in database
            if user is not None:
                print("User Exist")
                login(request,user) #passing request and user object
                return redirect('profile')
            else:
                print("User not Exist")
                form=AuthenticationForm()
                messages.success(request,'No account exist')
                return render(request,'login.html',{'form':form})
    else:
        print("Wrong method")
        form=AuthenticationForm()
        messages.success(request,'No account exist')
        #return render(request,'login.html',{'form':form})
    return render(request,'login.html',{'form':form})

def user_logout(request):
    logout(request)
    return redirect('login')
        
# def profile(request):     
#     if request.user.is_authenticated:
#         return render(request,'profile.html',{'user':request.user})      
#     else:
#         return redirect('login')

def profile(request): 
    if request.user.is_authenticated:
        #return redirect('profile')
        if request.method=="POST":
            form=ChangeUserData(request.POST,instance=request.user) #instance for change data of existing user 
            if form.is_valid():
                messages.success(request,'Account updated successfully')
                form.save()
                print(form.cleaned_data)
        else:
            form=ChangeUserData(instance=request.user)       
        #return redirect('profile')
        return render(request,'profile.html',{'form':form})
    else:
        return redirect('signup')
    
def pass_change(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form=PasswordChangeForm(user=request.user,data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request,form.user) #will update pass   # cleaned data is only for form fillup
                return redirect('profile')
        else:
            form=PasswordChangeForm(user=request.user)
        
        return render(request,'pass_change.html',{'form':form})
    else:
        return redirect('signup')

def pass_change2(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form=SetPasswordForm(user=request.user,data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request,form.user) #will update pass # cleaned data is only for form fillup
                return redirect('profile')
        else:
            form=SetPasswordForm(user=request.user)
        
        return render(request,'pass_change.html',{'form':form})
    else:
        return redirect('signup')
    
def change_user_data(request):
    if request.user.is_authenticated:
        #return redirect('profile')
        if request.method=="POST":
            form=ChangeUserData(request.POST,instance=request.user) #instance for change data of existing user 
            if form.is_valid():
                form.save()
                messages.success(request,'Changed successfully')
                print(form.cleaned_data)
                return redirect('profile')
        else:
            form=ChangeUserData(instance=request.user)      #it will show all previous data 
        #return redirect('profile')
        return render(request,'change_data.html',{'form':form})
    else:
        return redirect('signup')
