from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from inbox_app.utils import new_message, new_notification

from .forms import MentoringProgramForm, FeatureForm, UserResponseForm
from .models import MentoringProgram, Feature, UserResponse, UserEnroll, MmChat, MmTask
from .utils import get_myprogram_list, search_stuff, get_user_response_data, is_enroll_approved, eliminate_all_relation
from .utils import new_enroll_request, get_user_responses, approved_enroll_request, get_archivedprogram_list, assign_mentor_mentee
from .utils import get_mentor_data, get_mentee_data, program_strated_notifi

from user_app.models import Profile
from inbox_app.models import Notification


# ----------------------------------------------------------------
# MyPrograms views
# ----------------------------------------------------------------

@login_required(login_url='login')
def myprograms(request):
    myprogram_list = get_myprogram_list(request)
    context = {
        'myprograms':myprogram_list,
    }
    if request.user.is_authenticated:
        context['new_msg'] = new_message(request)
        context['new_notifi'] = new_notification(request)

    return render(request, 'mentoring_app/myprograms.html', context)


@login_required(login_url='login')
def archived_program(request):
    myprogram_list = get_archivedprogram_list(request)
    context = {
        'myprograms':myprogram_list,
    }
    if request.user.is_authenticated:
        context['new_msg'] = new_message(request)
        context['new_notifi'] = new_notification(request)

    return render(request, 'mentoring_app/archivedprogram.html', context)


# --------------------------------------------------------------------
# MentoringProgram Views
# --------------------------------------------------------------------

@login_required(login_url='login')
def mentoring_program(request, pk):
    program = MentoringProgram.objects.get(id=pk)

    if not program.is_published and program.admin.user.id != request.user.id:
        messages.error(request, "! Permission Denied !")
        return redirect('myprograms')

    trainers = program.trainer.all()
    moderators = program.moderator.all()
    all_feature = Feature.objects.filter(feature_program=program)
    try:
        enroll = UserEnroll.objects.get(user_profile=request.user.profile, userenroll_program=program)
    except Exception as e:
        print(e)
        enroll = None
    all_response, next_question, is_all_question_answered, is_enroll_inprogress = get_user_response_data(request, pk)
    enroll_request = new_enroll_request(request, pk)
    is_my_enroll_approved = is_enroll_approved(request, pk)

    try:
        enroll = UserEnroll.objects.get(user_profile=request.user.profile, userenroll_program=program)
        my_mentees = enroll.mentee.all()
        my_mentor = enroll.mentor
    except:
        my_mentees = None
        my_mentor = None
    context = {
        'my_mentor':my_mentor,
        'my_mentees':my_mentees,
        'is_my_enroll_approved':is_my_enroll_approved,
        'new_enroll_request': len(enroll_request),
        'enroll_inprogress':is_enroll_inprogress,
        'enroll':enroll,
        'program':program,
        'trainers':trainers,
        'moderators':moderators,
        'all_feature':all_feature,
        'new_msg':new_message(request),
        'new_notifi':new_notification(request),
    }
    return render(request, 'mentoring_app/mentoring_program.html', context)


@login_required(login_url='login')
def create_mentoring_program(request, pk):
    form = MentoringProgramForm()

    if request.method == 'POST':
        form = MentoringProgramForm(request.POST, request.FILES)
    
        if form.is_valid():
            form.save()

            program = form.instance
            program.admin = request.user.profile
            program.save()

            messages.success(request, "Mentoring Program Created Successfully")
            return redirect('mentoring_program', program.id)

    context = {
        'content': form, 
        'item_name':'MentoringProgram', 
        'create':True,
        'new_msg':new_message(request),
        'new_notifi':new_notification(request),
    }
    return render(request, 'mentoring_app/mentoring_data_form.html', context)

@login_required(login_url='login')
def update_mentoring_program(request, pk):
    program = MentoringProgram.objects.get(id=pk)

    if program.admin.user.id != request.user.id or program.is_archived or program.is_program_started:
        messages.error(request, "! Permission Denied !")
        return redirect('mentoring_program', program.id)

    form = MentoringProgramForm(instance=program)

    if request.method == 'POST':
        form = MentoringProgramForm(request.POST, request.FILES, instance=program)
    
        if form.is_valid():
            form.save()
            return redirect('mentoring_program', program.id)

    context = {
        'content': form, 
        'item_name':'MentoringProgram', 
        'update':True,    
        'new_msg':new_message(request),
        'new_notifi':new_notification(request),
    }
    return render(request, 'mentoring_app/mentoring_data_form.html', context)


@login_required(login_url='login')
def add_stuff(request, pk):
    profile_list, search_text = search_stuff(request)
    program = MentoringProgram.objects.get(id=pk)

    if program.admin.user.id != request.user.id or program.is_archived or program.is_program_started:
        messages.error(request, "! Permission Denied !")
        return redirect('mentoring_program', program.id)

    context = {
        'program': program,
        'profile_list': profile_list, 
        'search_text':search_text,
        'new_msg':new_message(request),
        'new_notifi':new_notification(request),
    }

    return render(request, 'mentoring_app/add_stuff.html', context)


@login_required(login_url='login')
def confirm_moderator(request, program_id, profile_id):
    program = MentoringProgram.objects.get(id=program_id)
    
    if program.admin.user.id != request.user.id or program.is_archived or program.is_program_started:
        messages.error(request, "! Permission Denied !")
        return redirect('mentoring_program', program.id)

    moderator = Profile.objects.get(id=profile_id)
    program.moderator.add(moderator)
    return redirect('mentoring_program', program.id)


@login_required(login_url='login')
def confirm_trainer(request, program_id, profile_id):
    program = MentoringProgram.objects.get(id=program_id)

    if program.admin.user.id != request.user.id or program.is_archived or program.is_program_started:
        messages.error(request, "! Permission Denied !")
        return redirect('mentoring_program', program.id)

    trainer = Profile.objects.get(id=profile_id)
    program.trainer.add(trainer)
    return redirect('mentoring_program', program.id)


@login_required(login_url='login')
def delete_moderator(request, program_id, profile_id):
    program = MentoringProgram.objects.get(id=program_id)

    if program.admin.user.id != request.user.id or program.is_archived or program.is_program_started:
        messages.error(request, "! Permission Denied !")
        return redirect('mentoring_program', program.id)

    moderator = Profile.objects.get(id=profile_id)
    program.moderator.remove(moderator)
    return redirect('mentoring_program', program.id)


@login_required(login_url='login')
def delete_trainer(request, program_id, profile_id):
    program = MentoringProgram.objects.get(id=program_id)

    if program.admin.user.id != request.user.id or program.is_archived or program.is_program_started:
        messages.error(request, "! Permission Denied !")
        return redirect('mentoring_program', program.id)

    trainer = Profile.objects.get(id=profile_id)
    program.trainer.remove(trainer)
    return redirect('mentoring_program', program.id)

@login_required(login_url='login')
def publish_program(request, program_id):
    program = MentoringProgram.objects.get(id=program_id)

    if program.admin.user.id != request.user.id or program.is_archived:
        messages.error(request, "! Permission Denied !")
        return redirect('mentoring_program', program.id)

    program.is_published = True
    program.save()
    return redirect('mentoring_program', program.id)

@login_required(login_url='login')
def unpublish_program(request, program_id):
    program = MentoringProgram.objects.get(id=program_id)

    if program.admin.user.id != request.user.id or program.is_archived:
        messages.error(request, "! Permission Denied !")
        return redirect('mentoring_program', program.id)

    program.is_published = False
    program.save()
    return redirect('mentoring_program', program.id)

@login_required(login_url='login')
def start_enroll(request, program_id):
    program = MentoringProgram.objects.get(id=program_id)

    if program.admin.user.id != request.user.id or program.is_archived:
        messages.error(request, "! Permission Denied !")
        return redirect('mentoring_program', program.id)

    program.is_enroll_on = True
    program.save()
    return redirect('mentoring_program', program.id)

@login_required(login_url='login')
def stop_enroll(request, program_id):
    program = MentoringProgram.objects.get(id=program_id)

    if program.admin.user.id != request.user.id or program.is_archived:
        messages.error(request, "! Permission Denied !")
        return redirect('mentoring_program', program.id)

    program.is_enroll_on = False
    program.save()
    return redirect('mentoring_program', program.id)

@login_required(login_url='login')
def start_program(request, program_id):
    program = MentoringProgram.objects.get(id=program_id)

    if program.admin.user.id != request.user.id or program.is_archived:
        messages.error(request, "! Permission Denied !")
        return redirect('mentoring_program', program.id)

    assign_mentor_mentee(request, program_id)

    program.is_program_started = True
    program.save()

    program_strated_notifi(request, program)
    
    return redirect('mentoring_program', program.id)

@login_required(login_url='login')
def stop_program(request, program_id):
    program = MentoringProgram.objects.get(id=program_id)

    if program.admin.user.id != request.user.id or program.is_archived:
        messages.error(request, "! Permission Denied !")
        return redirect('mentoring_program', program.id)

    eliminate_all_relation(request, program_id)

    program.is_program_started = False
    program.save()
    return redirect('mentoring_program', program.id)

@login_required(login_url='login')
def archive_program(request, program_id):
    program = MentoringProgram.objects.get(id=program_id)

    if program.admin.user.id != request.user.id or program.is_archived:
        messages.error(request, "! Permission Denied !")
        return redirect('mentoring_program', program.id)

    program.is_archived = True
    program.save()
    return redirect('mentoring_program', program.id)

# --------------------------------------------------------------------
# Feature Views
# --------------------------------------------------------------------

@login_required(login_url='login')
def add_feature(request, program_id):
    program = MentoringProgram.objects.get(id=program_id)
    form = FeatureForm()

    if program.admin.user.id != request.user.id or program.is_archived or program.is_program_started or program.is_enroll_on:
        messages.error(request, "! Permission Denied !")
        return redirect('mentoring_program', program.id)

    if request.method == 'POST':
        form = FeatureForm(request.POST)
    
        if form.is_valid():
            form.save()

            feature = form.instance
            feature.feature_program = program
            feature.save()

            return redirect('mentoring_program', program.id)

    context = {
        'content': form, 
        'item_name':'Featured Question', 
        'create':True,
        'new_msg':new_message(request),
        'new_notifi':new_notification(request),
    }
    return render(request, 'mentoring_app/mentoring_data_form.html', context)

@login_required(login_url='login')
def update_feature(request, program_id, feature_id):
    program = MentoringProgram.objects.get(id=program_id)
    feature = Feature.objects.get(id=feature_id)

    if program.admin.user.id != request.user.id or program.is_archived or program.is_program_started or program.is_enroll_on:
        messages.error(request, "! Permission Denied !")
        return redirect('mentoring_program', program.id)

    form = FeatureForm(instance=feature)

    if request.method == 'POST':
        form = FeatureForm(request.POST, instance=feature)
    
        if form.is_valid():
            form.save()
            return redirect('mentoring_program', program.id)

    context = {
        'content': form, 
        'item_name':'Featured Question', 
        'update':True,    
        'new_msg':new_message(request),
        'new_notifi':new_notification(request),
    }
    return render(request, 'mentoring_app/mentoring_data_form.html', context)

@login_required(login_url='login')
def delete_feature(request, program_id, feature_id):
    program = MentoringProgram.objects.get(id=program_id)

    if program.admin.user.id != request.user.id or program.is_archived or program.is_program_started or program.is_enroll_on:
        messages.error(request, "! Permission Denied !")
        return redirect('mentoring_program', program.id)

    feature = Feature.objects.get(id=feature_id)
    feature.delete()
    return redirect('mentoring_program', program.id)

# --------------------------------------------------------------------
#  UserEnroll Views
# --------------------------------------------------------------------


@login_required(login_url='login')
def user_enroll(request, program_id):
    program = MentoringProgram.objects.get(id=program_id)

    if program.is_archived or not program.is_enroll_on or program.admin.user.id == request.user.id:
        messages.error(request, "! Permission Denied !")
        return redirect('mentoring_program', program.id)
    
    form = UserResponseForm()
    all_response, next_question, is_all_question_answered, is_enroll_inprogress = get_user_response_data(request, program_id)

    try:
        enroll = UserEnroll.objects.get(user_profile=request.user.profile, userenroll_program=program)
    except Exception as e:
        print(e)
        enroll = UserEnroll(
            userenroll_program = program,
            user_profile = request.user.profile
        )
        enroll.save()

    if request.method == 'POST':
        form = UserResponseForm(request.POST)
    
        if form.is_valid():
            form.save()

            user_response = form.instance
            if user_response.exp_level > 10:
                user_response.exp_level = 10
            user_response.userresponse_profile = request.user.profile
            user_response.feature = next_question
            user_response.save()

            return redirect('user_enroll', program.id)

    context = {
        'enroll':enroll,
        'all_question_answered':is_all_question_answered,
        'next_question':next_question,
        'program':program,
        'all_response':all_response,
        'content': form, 
        'new_msg':new_message(request),
        'new_notifi':new_notification(request),
    }
    return render(request, 'mentoring_app/user_enroll.html', context)


@login_required(login_url='login')
def submit_for_review(request, program_id):
    program = MentoringProgram.objects.get(id=program_id)
    all_response, next_question, is_all_question_answered, is_enroll_inprogress = get_user_response_data(request, program_id)

    if program.admin.user.id == request.user.id or program.is_archived or program.is_program_started or not program.is_enroll_on or not is_all_question_answered:
        messages.error(request, "! Permission Denied !")
        return redirect('user_enroll', program.id)

    enroll = UserEnroll.objects.get(user_profile=request.user.profile, userenroll_program=program)
    enroll.is_submited = True
    enroll.save()

    return redirect('mentoring_program', program.id)


@login_required(login_url='login')
def update_response(request, program_id, response_id):
    response = UserResponse.objects.get(id=response_id)
    program = MentoringProgram.objects.get(id=program_id)

    if response.userresponse_profile.id != request.user.profile.id:
        messages.error(request, "! Permission Denied !")
        return redirect('user_enroll', program.id)

    form = UserResponseForm(instance=response)

    if request.method == 'POST':
        form = UserResponseForm(request.POST, instance=response)
    
        if form.is_valid():
            form.save()
            user_response = form.instance
            if user_response.exp_level > 10:
                user_response.exp_level = 10
            user_response.save()
            return redirect('user_enroll', program.id)

    context = {
        'content': form, 
        'item_name':'Update Your Response', 
        'update':True,    
        'new_msg':new_message(request),
        'new_notifi':new_notification(request),
    }
    return render(request, 'mentoring_app/mentoring_data_form.html', context)


@login_required(login_url='login')
def review_enroll(request, program_id):
    program = MentoringProgram.objects.get(id=program_id)
    moderators = program.moderator.all()

    if program.is_archived or program.is_program_started:
        messages.error(request, "! Permission Denied !")
        return redirect('mentoring_program', program.id)
    if request.user.profile not in moderators and program.admin.user.id != request.user.id:
        messages.error(request, "! Permission Denied !")
        return redirect('mentoring_program', program.id)
    

    enroll_requests = new_enroll_request(request, program_id)
    
    print("\n")
    print(enroll_requests)
    print("\n")

    context = {
        'enroll_requests':enroll_requests,
        'program':program,
        'new_msg':new_message(request),
        'new_notifi':new_notification(request),
    }
    return render(request, 'mentoring_app/review_enroll.html', context)


@login_required(login_url='login')
def review_user_enroll(request, enroll_id):
    enroll = UserEnroll.objects.get(id=enroll_id)
    program = MentoringProgram.objects.get(id=enroll.userenroll_program.id)
    moderators = program.moderator.all()

    if program.is_archived or program.is_program_started:
        messages.error(request, "! Permission Denied !")
        return redirect('mentoring_program', program.id)
    if request.user.profile not in moderators and program.admin.user.id != request.user.id:
        messages.error(request, "! Permission Denied !")
        return redirect('mentoring_program', program.id)
    
    all_response = get_user_responses(request, program.id, enroll.user_profile.id)
    context = {
        'enroll':enroll,
        'program':program,
        'all_response':all_response,
        'new_msg':new_message(request),
        'new_notifi':new_notification(request),
    }
    return render(request, 'mentoring_app/review_user_enroll.html', context)


@login_required(login_url='login')
def reject_enroll(request, enroll_id):
    enroll = UserEnroll.objects.get(id=enroll_id)
    program = MentoringProgram.objects.get(id=enroll.userenroll_program.id)
    moderators = program.moderator.all()

    if program.is_archived or program.is_program_started:
        messages.error(request, "! Permission Denied !")
        return redirect('mentoring_program', program.id)
    if request.user.profile not in moderators and program.admin.user.id != request.user.id:
        messages.error(request, "! Permission Denied !")
        return redirect('mentoring_program', program.id)
        
    enroll.is_submited = False
    enroll.is_approved = False
    enroll.save()

    notif = Notification.objects.create(
        title='Enrollment Request Rejected',
        description='Your request for enrollment in ' + enroll.userenroll_program.title + ' is rejected.',
        redirect_url=request.build_absolute_uri(redirect('mentoring_program', program.id).url),
        reciver=enroll.user_profile
    )
    notif.save()

    return redirect('review_enroll', enroll.userenroll_program.id)    


@login_required(login_url='login')
def approve_enroll(request, enroll_id):
    enroll = UserEnroll.objects.get(id=enroll_id)
    program = MentoringProgram.objects.get(id=enroll.userenroll_program.id)
    moderators = program.moderator.all()

    if program.is_archived or program.is_program_started:
        messages.error(request, "! Permission Denied !")
        return redirect('mentoring_program', program.id)
    if request.user.profile not in moderators and program.admin.user.id != request.user.id:
        messages.error(request, "! Permission Denied !")
        return redirect('mentoring_program', program.id)
    
    enroll.is_submited = False
    enroll.is_approved = True
    enroll.save()

    notif = Notification.objects.create(
        title='Enrollment Request Approved',
        description='Your request for enrollment in ' + enroll.userenroll_program.title + ' is Approved.',
        redirect_url=request.build_absolute_uri(redirect('mentoring_program', program.id).url),
        reciver=enroll.user_profile
    )
    notif.save()

    return redirect('review_enroll', enroll.userenroll_program.id)    


@login_required(login_url='login')
def approved_request(request, program_id):
    program = MentoringProgram.objects.get(id=program_id)
    moderators = program.moderator.all()

    if program.is_archived or program.is_program_started:
        messages.error(request, "! Permission Denied !")
        return redirect('mentoring_program', program.id)
    if request.user.profile not in moderators and program.admin.user.id != request.user.id:
        messages.error(request, "! Permission Denied !")
        return redirect('mentoring_program', program.id)
    
    approved_requests = approved_enroll_request(request, program_id)
    approved_requests_page = True

    context = {
        'approved_requests':approved_requests,
        'approved_requests_page':approved_requests_page,
        'program':program,
        'new_msg':new_message(request),
        'new_notifi':new_notification(request),
    }
    return render(request, 'mentoring_app/review_enroll.html', context)


@login_required(login_url='login')
def my_mentor(request, program_id):
    program = MentoringProgram.objects.get(id=program_id)

    if not program.is_program_started or program.admin.user.id == request.user.id:
        messages.error(request, "! Permission Denied !")
        return redirect('mentoring_program', program.id)
    
    text_messages, tasks, mentor = get_mentor_data(request, program)
    
    if request.method == 'POST':
        message = request.POST['message']
        msg = MmChat.objects.create(
            body = message,
            mmchat_program=program,
            mmchat_mentor=mentor,
            mmchat_mentee=request.user.profile,
            mmchat_sender = request.user.profile,
            mmchat_receiver = mentor
        )
        msg.save()
        return redirect('my_mentor', program.id)

    context = {
        'program':program,
        'text_messages':text_messages,
        'tasks':tasks,
        'receiver':mentor,
        'new_msg':new_message(request),
        'new_notifi':new_notification(request),
    }
    return render(request, 'mentoring_app/my_mentor.html', context)

@login_required(login_url='login')
def my_mentees(request, program_id, mentee_id):
    program = MentoringProgram.objects.get(id=program_id)
    mentee = Profile.objects.get(id=mentee_id)
    enroll = UserEnroll.objects.get(userenroll_program=program, user_profile=mentee)
    mentees = UserEnroll.objects.get(userenroll_program=program, user_profile=request.user.profile).mentee.all()

    if not program.is_program_started or program.admin.user.id == request.user.id:
        messages.error(request, "! Permission Denied !")
        return redirect('mentoring_program', program.id)
    
    text_messages, tasks = get_mentee_data(request, program, mentee)
    
    if request.method == 'POST':
        try:
            task_title = request.POST['task_title']
            task_description = request.POST['task_description']
            task_deadline = request.POST['task_deadline']
            if task_title != '' and task_description != '':
                task = MmTask.objects.create(
                    mmtask_program = program,
                    mmtask_mentor = request.user.profile,
                    mmtask_mentee = mentee,
                    title = task_title,
                    description = task_description,
                    deadline = task_deadline
                )
                task.save()
            else:
                message = request.POST['message']
                msg = MmChat.objects.create(
                    body = message,
                    mmchat_program=program,
                    mmchat_mentor=request.user.profile,
                    mmchat_mentee=mentee,
                    mmchat_sender = request.user.profile,
                    mmchat_receiver = mentee
                )
                msg.save()
        except :
            message = request.POST['message']
            msg = MmChat.objects.create(
                body = message,
                mmchat_program=program,
                mmchat_mentor=request.user.profile,
                mmchat_mentee=mentee,
                mmchat_sender = request.user.profile,
                mmchat_receiver = mentee
            )
            msg.save()
        return redirect('my_mentees', program.id, mentee.id)

    context = {
        'active_mentee':mentee,
        'program':program,
        'text_messages':text_messages,
        'tasks':tasks,
        'mentees':mentees,
        'new_msg':new_message(request),
        'new_notifi':new_notification(request),
    }
    return render(request, 'mentoring_app/my_mentees.html', context)




