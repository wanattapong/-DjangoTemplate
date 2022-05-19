from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseServerError
from django.contrib.sessions.models import Session
from account.models import User
from settings.helper import encode_url
from django.core.files.storage import default_storage

# Create your views here.

from .serializers import UserSerializer
# from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework import status, viewsets, generics
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer


""" API Here """

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]

""" ENd API """


def is_admin(request):
    user = request.user.groups.all()
    if user[0].name == 'Admin' and request.user.is_authenticated:
        return True
    else:
        return False

def get_User_login():
    user_online = []
    for session_ in Session.objects.all():
        session_.get_decoded()
        if session_.get_decoded() not in [None, {}, 'Session data corruptedclear']:
            if User.objects.get(id=session_.get_decoded()['_auth_user_id']) not in user_online:
                user_online.append(User.objects.get(id=session_.get_decoded()['_auth_user_id']))
        else:
            # delete session if session data is corrupted
            session_.delete()
    return user_online

@login_required()
def index(request):
    try:
        if is_admin(request):
            context = {
                'user_all': User.objects.all().count(),
                'user_online': get_User_login(),
            }
            return render(request, 'home.html', context)
        else:
            return redirect('logout')
    except Exception as e:
        return HttpResponseServerError
    finally:
        print('=== end ibiobank main curator ===')

@login_required()
def manage_user(request):
    try:
        if is_admin(request):
            user = User.objects.all().values()
            for i in user:
                i['id'] = encode_url(i['id'])
            context = {
                'users': user,
            }
            return render(request, 'manage_user.html', context)
        else:
            return redirect('logout')
    except Exception as e:
        return HttpResponseServerError(e)
    finally:
        print('=== end ibiobank main curator ===')

def manage_user_detail(request, username):
    try:
        if is_admin(request):
            user = User.objects.get(username=username)
            print(user)
            context = {
                'user': user,
            }
            return render(request, 'manage_user_detail.html', context)
        else:
            return redirect('logout')
    except Exception as e:
        return HttpResponseServerError(e)
    finally:
        print('=== end ibiobank main curator ===')

def manage_user_delete(request, username):
    try:
        if is_admin(request):
            user = User.objects.get(username=username)
            if default_storage.exists(user.avatar.path) == True:
                default_storage.delete(user.avatar.path)
            user.delete()
            return redirect('manage_user')
        else:
            return redirect('logout')
    except Exception as e:
        return HttpResponseServerError(e)
    finally:
        print('=== end ibiobank main curator ===')