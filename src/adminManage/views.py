from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseServerError
from django.contrib.sessions.models import Session
from account.models import User

# Create your views here.

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