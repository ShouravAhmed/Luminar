
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect

from .models import MentoringProgram, UserEnroll, Feature, UserResponse, MmChat, MmTask
from user_app.models import Profile
from inbox_app.models import Notification

def get_myprogram_list(request):   
    myprogram_list = MentoringProgram.objects.distinct().filter(
        Q(admin = request.user.profile) |
        Q(trainer = request.user.profile) |
        Q(moderator = request.user.profile) |
        Q(userenroll_program__in = UserEnroll.objects.filter(user_profile = request.user.profile, is_approved=True))
    ).filter(is_archived=False)
    return myprogram_list

def get_archivedprogram_list(request):   
    myprogram_list = MentoringProgram.objects.distinct().filter(
        Q(admin = request.user.profile) |
        Q(trainer = request.user.profile) |
        Q(moderator = request.user.profile) |
        Q(userenroll_program__in = UserEnroll.objects.filter(user_profile = request.user.profile, is_approved=True))
    ).filter(is_archived=True)
    return myprogram_list

def search_stuff(request):
    search_text = ''
    if request.GET.get('search_text'):
        search_text = request.GET.get('search_text')
        
    profiles = Profile.objects.distinct().order_by('created_at').filter(is_verified=True).filter(
        Q(username__icontains = search_text) |
        Q(name__icontains = search_text)
    )

    return profiles, search_text

def get_user_response_data(request, program_id):
    program = MentoringProgram.objects.get(id=program_id)
    features = Feature.objects.filter(feature_program=program)
    all_response = list()
    next_question = None

    for feature in features:
        if UserResponse.objects.filter(feature=feature, userresponse_profile=request.user.profile).exists():
            response = UserResponse.objects.get(feature=feature, userresponse_profile=request.user.profile)
            all_response.append(response)
        else:
            if next_question is None:
                next_question = feature
    is_all_question_answered = (len(all_response) == len(features))
    is_enroll_inprogress = (len(all_response) != len(features) and len(all_response) > 0)
    return all_response, next_question, is_all_question_answered, is_enroll_inprogress

def new_enroll_request(request, program_id):
    program = MentoringProgram.objects.get(id=program_id)
    return UserEnroll.objects.filter(userenroll_program=program, is_submited=True)

def get_user_responses(request, program_id, user_id):
    program = MentoringProgram.objects.get(id=program_id)
    features = Feature.objects.filter(feature_program=program)
    profile = Profile.objects.get(id=user_id)
    
    all_response = list()
    
    for feature in features:
        if UserResponse.objects.filter(feature=feature, userresponse_profile=profile).exists():
            response = UserResponse.objects.get(feature=feature, userresponse_profile=profile)
            all_response.append(response)
    return all_response

def approved_enroll_request(request, program_id):
    program = MentoringProgram.objects.get(id=program_id)
    return UserEnroll.objects.filter(userenroll_program=program, is_approved=True)

def is_enroll_approved(request, program_id):
    program = MentoringProgram.objects.get(id=program_id)
    try:
        enroll = UserEnroll.objects.get(user_profile=request.user.profile, userenroll_program=program)
        return enroll.is_approved
    except:
        return False

def eliminate_all_relation(request, program_id):
    program = MentoringProgram.objects.get(id=program_id)
    enrolls =  UserEnroll.objects.filter(userenroll_program=program)
    for enroll in enrolls:
        mentees = enroll.mentee.all()
        for mentee in mentees:
            enroll.mentee.remove(mentee)
        enroll.mentor = None

def matching_score(program, mntor, mntee):
    all_feature = Feature.objects.filter(feature_program=program)
    ret = 0
    for fetr in all_feature:
        mentor_responses = UserResponse.objects.get(feature=fetr, userresponse_profile=mntor.user_profile)
        mentee_responses = UserResponse.objects.get(feature=fetr, userresponse_profile=mntee.user_profile)
        ret += min(mentor_responses.exp_level, mentee_responses.exp_level)
    return ret

def mentor_assigned_notifi(request, program, mentor, mentee):
    notif = Notification.objects.create(
        title='Mentor assigned | '+program.title,
        description= mentor.name+' is assigned for you as a mentor in ' + program.title,
        redirect_url=request.build_absolute_uri(redirect('mentoring_program', program.id).url),
        reciver=mentee
    )
    notif.save()
    notif = Notification.objects.create(
        title='Mentee assigned | '+program.title,
        description= mentee.name+' is assigned to you as a mentee in ' + program.title,
        redirect_url=request.build_absolute_uri(redirect('mentoring_program', program.id).url),
        reciver=mentor
    )
    notif.save()

def program_strated_notifi(request, program):
    enrolls =  UserEnroll.objects.filter(userenroll_program=program, is_approved=True)
    moderators = program.moderator.all()
    for enroll in enrolls:
        notif = Notification.objects.create(
            title='Mentoring Prgram started',
            description='Your Mentoring Program'+program.title+' is started',
            redirect_url=request.build_absolute_uri(redirect('mentoring_program', program.id).url),
            reciver=enroll.user_profile
        )
        notif.save()
    for moderator in moderators:
        notif = Notification.objects.create(
            title='Mentoring Prgram started',
            description='Your Mentoring Program'+program.title+' is started',
            redirect_url=request.build_absolute_uri(redirect('mentoring_program', program.id).url),
            reciver=moderator
        )
        notif.save()


def assign_mentor_mentee(request, program_id):
    program = MentoringProgram.objects.get(id=program_id)
    enrolls =  UserEnroll.objects.filter(userenroll_program=program, is_approved=True)
    trainers = program.trainer.all()
    is_taken = dict()
    que = []
    for trainer in trainers:
        try:
            trainer_enroll = UserEnroll.objects.get(userenroll_program=program, user_profile=trainer)
            if trainer_enroll.is_approved:
                is_taken[trainer_enroll] = True
                que.append(trainer_enroll)
        except:
            pass
    while len(que) > 0:
        mntor = que.pop(0) 
        for i in range(5):
            mx = 0
            mntee = None
            for mnt in enrolls:
                if mnt not in is_taken:
                    score = matching_score(program, mntor, mnt)
                    if score > mx:
                        mx = score
                        mntee = mnt
            if mntee:
                is_taken[mntee] = True
                que.append(mntee)
                mntor.mentee.add(mntee.user_profile)
                mntee.mentor = mntor.user_profile
                mntor.save()
                mntee.save()

                mentor_assigned_notifi(request, program, mntor.user_profile, mntee.user_profile)

                print("\n---------------------------------")
                print("connected")
                print("---------------------------------")
                print('mentor:', mntor) 
                print("---------------------------------\n")
                print('mentee:', mntee)
                print("---------------------------------\n")

def get_mentor_data(request, program):
    enroll = UserEnroll.objects.get(userenroll_program=program, user_profile=request.user.profile)
    mentor = enroll.mentor
    text_messages = MmChat.objects.distinct().order_by('created_at').filter(
        Q(mmchat_sender=request.user.profile, mmchat_receiver=mentor, mmchat_program=program, mmchat_mentor=mentor, mmchat_mentee=request.user.profile) |
        Q(mmchat_sender=mentor, mmchat_receiver=request.user.profile, mmchat_program=program, mmchat_mentor=mentor, mmchat_mentee=request.user.profile)
    )
    for msg in text_messages:
        if msg.mmchat_sender != request.user.profile:
            msg.is_read = True
            msg.save()
    tasks = MmTask.objects.order_by('created_at').filter(
        mmtask_program = program,
        mmtask_mentor = mentor,
        mmtask_mentee = request.user.profile,
    )
    return text_messages, tasks, mentor

def get_mentee_data(request, program, mentee):
    mentor = request.user.profile
    
    text_messages = MmChat.objects.distinct().order_by('created_at').filter(
        Q(mmchat_sender=mentee, mmchat_receiver=mentor, mmchat_program=program, mmchat_mentor=mentor, mmchat_mentee=mentee) |
        Q(mmchat_sender=mentor, mmchat_receiver=mentee, mmchat_program=program, mmchat_mentor=mentor, mmchat_mentee=mentee)
    )
    for msg in text_messages:
        if msg.mmchat_sender != mentor:
            msg.is_read = True
            msg.save()
    tasks = MmTask.objects.order_by('created_at').filter(
        mmtask_program = program,
        mmtask_mentor = mentor,
        mmtask_mentee = mentee,
    )
    return text_messages, tasks

