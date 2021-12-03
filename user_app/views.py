from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from .models import Profile, Skill, Achivement, Project, Interest, Exprience
# from mentor_app.models import MentoringPrograms
from .forms import UserRegistrationForm, ProfileForm, SkillForm
from .forms import ExprienceForm, AchivementForm, ProjectForm, InterestForm
from .utils import search_profile, paginate_profile


def dashboard(request):
    context = {}
    return render(request, 'user_app/dashboard.html', context)


# --------------------------------------------------------------------
# User & Profile Views
# --------------------------------------------------------------------
@login_required(login_url='login')
def profiles(request):
    profile_list, search_text = search_profile(request)

    profile_per_page = 6
    pagination_preview = 3
    current_page_profile_list, custom_pagination_range = paginate_profile(request, profile_list, profile_per_page, pagination_preview)

    context = {
        'profile_list': current_page_profile_list, 
        'custom_pagination_range': custom_pagination_range, 
        'search_text':search_text
    }

    return render(request, 'user_app/all_users.html', context)


@login_required(login_url='login')
def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    # mentoring_programs = MentoringPrograms.objects.filter(member=pk)
    skills = Skill.objects.filter(owner=pk)
    expriences = Exprience.objects.filter(owner=pk)
    achivements = Achivement.objects.filter(owner=pk)
    projects = Project.objects.filter(owner=pk)
    interests = Interest.objects.filter(owner=pk)

    context = {
        'profile':profile,
        'skills':skills,
        'expriences':expriences,
        'achivements':achivements, 
        'projects': projects, 
        'interests':interests, 
        # 'mentoring_programs':mentoring_programs
    }
    return render(request, 'user_app/user_profile.html', context)

def login_user(request):
    if request.user.is_authenticated:
        messages.error(request, 'You Are Already Loged In')
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']
        try:
            user_data = User.objects.get(username=username)
            if not user_data.profile.is_verified:
                messages.warning(request, "Please check your email and Verify your account.")
                return redirect('login')
        except:
            messages.error(request, "Username Does Not Exist.")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "✨✨ 🔥Welcome Aboard : "+ username +"🔥 ✨✨")
            return redirect('dashboard')
        else:
            messages.error(request, "Username or Password is Incorrect")

    context = {}
    return render(request, 'user_app/login_register.html', context)

@login_required(login_url='login')
def logout_user(request):
    username = str(request.user.profile.name)
    logout(request)
    messages.info(request, username + " : Loged Out Successfully." )
    return redirect('login')

def register_user(request):
    if request.user.is_authenticated:
        messages.error(request, 'You Are Already Loged In')
        return redirect('dashboard')
    
    form = UserRegistrationForm()

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.email = user.email.lower()
            user.save()

            messages.success(request, "🎉🎉 Registration Successful 🎉🎉")
            return redirect('varify_account')

    context = {'register':True, 'form':form}
    return render(request, 'user_app/login_register.html', context)

def varify_account(request):
    context = {'varify_account':True}
    return render(request, 'user_app/varify_account.html', context)

def varify_account_success(request, pk):
    context = {'varify_account_success':True}
    try:
        profile = Profile.objects.get(id=pk)
        if profile:
            if profile.is_verified:
                context['verified'] = True
            else:
                profile.is_verified = True
                profile.save()
        else:
            context['not_valid'] = True
    except :
        context['not_valid'] = True
    
    return render(request, 'user_app/varify_account.html', context)

@login_required(login_url='login')
def update_profile(request, pk):
    profile = Profile.objects.get(id=pk)

    if profile.user.id != request.user.id:
        messages.error(request, "This Is Not Your Profile 😜")
        return redirect('user_profile', pk)

    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile', pk)

    context = {'form': form, 'profile':profile, 'update':True}
    return render(request, 'user_app/edit_profile.html', context)


# --------------------------------------------------------------------
# Skill Views
# --------------------------------------------------------------------
@login_required(login_url='login')
def create_skill(request):
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            form.save()

            skill = form.instance
            skill.owner = request.user.profile
            skill.save()

            messages.success(request, "Skill is Created Successfully")
            return redirect('user_profile', request.user.profile.id)

    context = {'content': form, 'item_name':'Skill', 'create':True}
    return render(request, 'user_app/user_data_form.html', context)

@login_required(login_url='login')
def update_skill(request, pk):
    skill = Skill.objects.get(id=pk)

    if skill.owner.user.id != request.user.id:
        messages.error(request, "This Is Not Your SKill 😜")
        return redirect('user_profile', skill.owner.id)

    form = SkillForm(instance=skill)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('user_profile', skill.owner.id)

    context = {'content': form, 'item_name':'Skill', 'update':True}
    return render(request, 'user_app/user_data_form.html', context)

@login_required(login_url='login')
def delete_skill(request, pk):
    skill = Skill.objects.get(id=pk)

    if skill.owner.user.id != request.user.id:
        messages.error(request, "This Is Not Your SKill 😜")
        return redirect('user_profile', skill.owner.id)

    if request.method == 'POST':
        skill.delete()
        return redirect('user_profile', skill.owner.id)

    context = {'content': skill, 'item_name':'Skill', 'delete':True}
    return render(request, 'user_app/user_data_form.html', context)


# --------------------------------------------------------------------
# Exprience Views
# --------------------------------------------------------------------
@login_required(login_url='login')
def create_exprience(request):
    form = ExprienceForm()
    if request.method == 'POST':
        form = ExprienceForm(request.POST)
        if form.is_valid():
            form.save()

            exp = form.instance
            exp.owner = request.user.profile
            exp.save()

            messages.success(request, "Exprience is Created Successfully")
            return redirect('user_profile', request.user.profile.id)

    context = {'content': form, 'item_name':'Exprience', 'create':True}
    return render(request, 'user_app/user_data_form.html', context)

@login_required(login_url='login')
def update_exprience(request, pk):
    exprience = Exprience.objects.get(id=pk)

    if exprience.owner.user.id != request.user.id:
        messages.error(request, "This Is Not Your SKill 😜")
        return redirect('user_profile', exprience.owner.id)

    form = ExprienceForm(instance=exprience)
    if request.method == 'POST':
        form = ExprienceForm(request.POST, instance=exprience)
        if form.is_valid():
            form.save()
            return redirect('user_profile', exprience.owner.id)

    context = {'content': form, 'item_name':'Exprience', 'update':True}
    return render(request, 'user_app/user_data_form.html', context)

@login_required(login_url='login')
def delete_exprience(request, pk):
    exprience = Exprience.objects.get(id=pk)

    if exprience.owner.user.id != request.user.id:
        messages.error(request, "This Is Not Your SKill 😜")
        return redirect('user_profile', exprience.owner.id)

    if request.method == 'POST':
        exprience.delete()
        return redirect('user_profile', exprience.owner.id)

    context = {'content': exprience, 'item_name':'Exprience', 'delete':True}
    return render(request, 'user_app/user_data_form.html', context)


# --------------------------------------------------------------------
# Achivement Views
# --------------------------------------------------------------------
@login_required(login_url='login')
def create_achivement(request):
    form = AchivementForm()
    if request.method == 'POST':
        form = AchivementForm(request.POST)
        if form.is_valid():
            form.save()

            achivement = form.instance
            achivement.owner = request.user.profile
            achivement.save()

            messages.success(request, "Achivement is Created Successfully")
            return redirect('user_profile', request.user.profile.id)

    context = {'content': form, 'item_name':'Achivement', 'create':True}
    return render(request, 'user_app/user_data_form.html', context)

@login_required(login_url='login')
def update_achivement(request, pk):
    achivement = Achivement.objects.get(id=pk)

    if achivement.owner.user.id != request.user.id:
        messages.error(request, "This Is Not Your SKill 😜")
        return redirect('user_profile', achivement.owner.id)

    form = AchivementForm(instance=achivement)
    if request.method == 'POST':
        form = AchivementForm(request.POST, instance=achivement)
        if form.is_valid():
            form.save()
            return redirect('user_profile', achivement.owner.id)

    context = {'content': form, 'item_name':'Achivement', 'update':True}
    return render(request, 'user_app/user_data_form.html', context)

@login_required(login_url='login')
def delete_achivement(request, pk):
    achivement = Achivement.objects.get(id=pk)

    if achivement.owner.user.id != request.user.id:
        messages.error(request, "This Is Not Your SKill 😜")
        return redirect('user_profile', achivement.owner.id)

    if request.method == 'POST':
        achivement.delete()
        return redirect('user_profile', achivement.owner.id)

    context = {'content': achivement, 'item_name':'Achivement', 'delete':True}
    return render(request, 'user_app/user_data_form.html', context)


# --------------------------------------------------------------------
# Project Views
# --------------------------------------------------------------------
@login_required(login_url='login')
def create_project(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()

            project = form.instance
            project.owner = request.user.profile
            project.save()

            messages.success(request, "Project is Created Successfully")
            return redirect('user_profile', request.user.profile.id)

    context = {'content': form, 'item_name':'Project', 'create':True}
    return render(request, 'user_app/user_data_form.html', context)

@login_required(login_url='login')
def update_project(request, pk):
    project = Project.objects.get(id=pk)

    if project.owner.user.id != request.user.id:
        messages.error(request, "This Is Not Your SKill 😜")
        return redirect('user_profile', project.owner.id)

    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('user_profile', project.owner.id)

    context = {'content': form, 'item_name':'Project', 'update':True}
    return render(request, 'user_app/user_data_form.html', context)

@login_required(login_url='login')
def delete_project(request, pk):
    project = Project.objects.get(id=pk)

    if project.owner.user.id != request.user.id:
        messages.error(request, "This Is Not Your SKill 😜")
        return redirect('user_profile', project.owner.id)

    if request.method == 'POST':
        project.delete()
        return redirect('user_profile', project.owner.id)

    context = {'content': project, 'item_name':'Project', 'delete':True}
    return render(request, 'user_app/user_data_form.html', context)


# --------------------------------------------------------------------
# Interest Views
# --------------------------------------------------------------------
@login_required(login_url='login')
def create_interest(request):
    form = InterestForm()
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            form.save()

            interest = form.instance
            interest.owner = request.user.profile
            interest.save()

            messages.success(request, "Interest is Created Successfully")
            return redirect('user_profile', request.user.profile.id)

    context = {'content': form, 'item_name':'Interest', 'create':True}
    return render(request, 'user_app/user_data_form.html', context)

@login_required(login_url='login')
def update_interest(request, pk):
    interest = Interest.objects.get(id=pk)

    if interest.owner.user.id != request.user.id:
        messages.error(request, "This Is Not Your SKill 😜")
        return redirect('user_profile', interest.owner.id)

    form = InterestForm(instance=interest)
    if request.method == 'POST':
        form = InterestForm(request.POST, instance=interest)
        if form.is_valid():
            form.save()
            return redirect('user_profile', interest.owner.id)

    context = {'content': form, 'item_name':'Interest', 'update':True}
    return render(request, 'user_app/user_data_form.html', context)

@login_required(login_url='login')
def delete_interest(request, pk):
    interest = Interest.objects.get(id=pk)

    if interest.owner.user.id != request.user.id:
        messages.error(request, "This Is Not Your SKill 😜")
        return redirect('user_profile', interest.owner.id)

    if request.method == 'POST':
        interest.delete()
        return redirect('user_profile', interest.owner.id)

    context = {'content': interest, 'item_name':'Interest', 'delete':True}
    return render(request, 'user_app/user_data_form.html', context)


# --------------------------------------------------------------------
# --------------------------------------------------------------------