from django.urls import path
from .views import create_mentoring_program, myprograms, add_stuff, confirm_trainer, confirm_moderator
from .views import update_mentoring_program, mentoring_program, delete_trainer, delete_moderator
from .views import unpublish_program, publish_program
from .views import start_enroll, stop_enroll, start_program, stop_program, archive_program
from .views import add_feature, update_feature, delete_feature, submit_for_review
from .views import user_enroll, update_response, review_enroll, review_user_enroll
from .views import reject_enroll, approve_enroll, approved_request, archived_program
from .views import my_mentor, my_mentees

urlpatterns = [
    path('myprograms/', myprograms, name='myprograms'),
    path('myprograms/archivedprogram', archived_program, name='archived_program'),
    path('myprograms/<str:pk>/', mentoring_program, name='mentoring_program'),
    path('myprograms/create/<str:pk>/', create_mentoring_program, name='create_program'),
    path('myprograms/<str:pk>/update/', update_mentoring_program, name='update_program'),
    
    path('myprograms/<str:pk>/addstuff/', add_stuff, name='add_stuff'),
    
    path('myprograms/<str:program_id>/confirmtrainer/<str:profile_id>/', confirm_trainer, name='confirm_trainer'),
    path('myprograms/<str:program_id>/confirmmoderator/<str:profile_id>/', confirm_moderator, name='confirm_moderator'),
    
    path('myprograms/<str:program_id>/deletetrainer/<str:profile_id>/', delete_trainer, name='delete_trainer'),
    path('myprograms/<str:program_id>/deletemoderator/<str:profile_id>/', delete_moderator, name='delete_moderator'),
    
    path('myprograms/<str:program_id>/publishprogram/', publish_program, name='publish_program'),
    path('myprograms/<str:program_id>/unpublishprogram/', unpublish_program, name='unpublish_program'),
    
    path('myprograms/<str:program_id>/startenroll/', start_enroll, name='start_enroll'),
    path('myprograms/<str:program_id>/stopenroll/', stop_enroll, name='stop_enroll'),
    
    path('myprograms/<str:program_id>/startprogram/', start_program, name='start_program'),
    path('myprograms/<str:program_id>/stopprogram/', stop_program, name='stop_program'),
    
    path('myprograms/<str:program_id>/archiveprogram/', archive_program, name='archive_program'),

    path('myprograms/<str:program_id>/addfeature/', add_feature, name='add_feature'),
    path('myprograms/<str:program_id>/updatefeature/<str:feature_id>/', update_feature, name='update_feature'),
    path('myprograms/<str:program_id>/deletefeature/<str:feature_id>/', delete_feature, name='delete_feature'),

    path('myprograms/<str:program_id>/userenroll/', user_enroll, name='user_enroll'),
    path('myprograms/<str:program_id>/submitforreview/', submit_for_review, name='submit_for_review'),
    
    path('myprograms/<str:program_id>/updateresponse/<str:response_id>/', update_response, name='update_response'),
    path('myprograms/<str:program_id>/reviewenroll/', review_enroll, name='review_enroll'),
    
    path('myprograms/<str:enroll_id>/reviewuserenroll/', review_user_enroll, name='review_user_enroll'),
    path('myprograms/<str:enroll_id>/rejectenroll/', reject_enroll, name='reject_enroll'),

    path('myprograms/<str:enroll_id>/approveenroll/', approve_enroll, name='approve_enroll'),
    path('myprograms/<str:program_id>/approvedrequest/', approved_request, name='approved_request'),

    path('myprograms/<str:program_id>/mymentor/', my_mentor, name='my_mentor'),
    path('myprograms/<str:program_id>/mymentees/<str:mentee_id>/', my_mentees, name='my_mentees'),
]

