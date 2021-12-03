
from .models import Profile, Skill, Exprience, Achivement, Project, Interest

from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings



def search_profile(request):
    search_text = ''
    if request.GET.get('search_text'):
        search_text = request.GET.get('search_text')
        
    profiles = Profile.objects.distinct().order_by('created_at').filter(is_verified=True).filter(
        Q(username__icontains = search_text) |
        Q(name__icontains = search_text) |
        Q(intro__icontains = search_text) |
        Q(location__icontains = search_text) |
        Q(skill__in = Skill.objects.filter(title__icontains=search_text)) |
        Q(exprience__in = Exprience.objects.filter(
                Q(organization__icontains=search_text) |
                Q(role__icontains=search_text)
            )
        ) |
        Q(achivement__in = Achivement.objects.filter(title__icontains=search_text)) |
        Q(project__in = Project.objects.filter(title__icontains=search_text)) |
        Q(interest__in = Interest.objects.filter(title__icontains=search_text))
    )

    return profiles, search_text

def paginate_profile(request, profile_list, profile_per_page, pagination_preview):

    paginator = Paginator(profile_list, profile_per_page)
    page_no = request.GET.get('page')
    
    try:
        current_page_profile_list = paginator.page(page_no)
    except PageNotAnInteger:
        page_no = 1
        current_page_profile_list = paginator.page(page_no)
    except EmptyPage:
        page_no = paginator.num_pages
        current_page_profile_list = paginator.page(paginator.num_pages)
    except:
        page_no = 1
        current_page_profile_list = paginator.page(page_no)

    page_no = int(page_no)
    start_page = max(page_no - pagination_preview, 1)
    end_page = min(page_no + pagination_preview, paginator.num_pages) + 1

    if page_no <= pagination_preview:
        end_page = min(end_page + pagination_preview - page_no + 1, paginator.num_pages + 1)

    if page_no > paginator.num_pages - pagination_preview:
        start_page = max(start_page - (pagination_preview - (paginator.num_pages - page_no + 1) + 1), 1)

    custom_pagination_range = range(start_page, end_page)

    return current_page_profile_list, custom_pagination_range

def luminar_email(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        recipient_list,
        fail_silently=False,
    )

def account_varification_email(profile_id, user_email):
    context={'profile_id':profile_id}
    html_content = render_to_string('user_app/varify_ac_email.html', context)
    text_content = strip_tags(html_content)
    subject = "Account Varification Email"
    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.EMAIL_HOST_USER,
        [user_email, ]
    )
    email.attach_alternative(html_content, 'text/html')
    email.send()

