from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.MemberListView.as_view(), name='company_members_list'),
    path('delete/<int:id>/', views.MemberListView.as_view(), name='company_member_delete'),
    path('invite/', views.InviteView.as_view(), name='company_members_invite'),
    path('invite/<uuid:token>', views.InviteView.as_view(), name='company_members_invite_token'),
]
