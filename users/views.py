from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from .forms import *
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
    if request.user.is_authenticated: #already logged in
        return redirect('profile')
    return render(request,'signup_types.html')

def doctor_signup(request):
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.title='Dr.'
            user.profile_picture = request.FILES['profile_picture']
            user.is_staff=True
            user.save()  
            login(request, user)
            messages.success(request, 'Doctor Account Created Successfully')
            return redirect('profile')
            
            # if 'profile_picture' in request.FILES:
            #     user.profile_picture = request.FILES['profile_picture']
            #     user.save()  
            
            
            # user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            # if user is not None:
            #     login(request, user)
            #     messages.success(request, 'Doctor Account Created Successfully')
            #     # return redirect('profile')
            #     return render(request,'profile.html',{'user':user})
            # else:
            #     messages.error(request, 'Failed to authenticate user.')
            #     return redirect('login')  
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
            user.title='Dr.'
            user.save()  
            login(request, user)
            messages.success(request, 'Patient Account Created Successfully')
            return redirect('profile')
            
            # if 'profile_picture' in request.FILES:
            #     user.profile_picture = request.FILES['profile_picture']
            #     user.save()  
            
            # messages.success(request, 'Patient Account Created Successfully')
            
            # user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            # if user is not None:
            #     login(request, user)
            #     # return redirect('profile')
            #     return render(request,'profile.html',{'user':user})
            # else:
            #     messages.error(request, 'Failed to authenticate user.')
                
            #     return redirect('login')  
        else:
            messages.error(request, 'Form validation failed.')
    else:
        form = RegisterForm()
    
    return render(request, "signup.html", {'form': form})

def login_page(request):
    if request.user.is_authenticated: #already logged in
        return redirect('profile')
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

# def profile(request): 
#     if request.user.is_authenticated:
#         #return redirect('profile')
#         if request.method=="POST":
#             form=ChangeUserData(request.POST,instance=request.user) #instance for change data of existing user 
#             if form.is_valid():
#                 messages.success(request,'Account updated successfully')
#                 form.save()
#                 print(form.cleaned_data)
#         else:
#             form=ChangeUserData(instance=request.user)       
#         #return redirect('profile')
#         return render(request,'profile.html',{'form':form})
#     else:
#         return redirect('signup')


def profile(request):
    if request.user.is_authenticated:
        return render(request,'profile.html',{'user':request.user})
    else:
        return redirect('login')
    
    

def create_post(request):
    if not request.user.is_staff:
        return redirect('home')
    
    if request.method == 'POST':
        form = Create_Blog(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.userprofile = request.user
            blog.save()
            return redirect('my_blogs')
    else:
        form = Create_Blog()
    return render(request, 'create_blog.html', {'form': form})

# def blog_list(request):
#     if not request.user.is_authenticated:
#         return redirect('login')
#     blogs=Blog.objects.filter(save_as_draft=False)
#     return render(request,'blog_list.html',{'blogs':blogs})


def blog_list(request):
    categories = [category[0] for category in Blog.CATEGORIES]
    selected_category = request.GET.get('category')

    if selected_category and selected_category != 'All Categories':
        blogs = Blog.objects.filter(category=selected_category, save_as_draft=False)
    else:
        blogs = Blog.objects.filter(save_as_draft=False)

    return render(request, 'blog_list.html', {'blogs': blogs, 'categories': categories})


def my_blogs(request):
    if not request.user.is_staff:
        return redirect('blog_list')
    blogs = request.user.blogs.all() 
    return render(request, 'my_blogs.html', {'blogs': blogs})

def blog_details(request, pk):
    try:
        blog = Blog.objects.get(pk=pk)
        if blog.userprofile != request.user:
            return redirect('blog_list')
        return render(request, 'blog_details.html', {'blog': blog})
    except Blog.DoesNotExist:
        return redirect('blog_list')

def edit_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.user != blog.userprofile:
        return redirect('blog_list')

    if request.method == 'POST':
        form = Create_Blog(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('my_blogs')
    else:
        form = Create_Blog(instance=blog)

    return render(request, 'edit_blog.html', {'form': form})

def delete_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.user != blog.userprofile:
        return redirect('blog_list')
    blog.delete()
    return redirect('blog_list')

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
