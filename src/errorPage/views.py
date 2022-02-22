from django.shortcuts import render

# Create your views here.

def my_custom_bad_request_view(request, *args, **argv):
    return render(request, '400.html', status=400)

def my_custom_permission_denied_view(request, *args, **argv):
    return render(request, '403.html', status=403)
    
def my_custom_page_not_found_view(request, *args, **argv):
    return render(request, '404.html', status=404)

def my_custom_error_view(request, *args, **argv):
    return render(request, '500.html', status=500)

# and add this to url.py in settings:

# handler404 = 'errorPage.views.my_custom_page_not_found_view'
# handler500 = 'errorPage.views.my_custom_error_view'
# handler403 = 'errorPage.views.my_custom_permission_denied_view'
# handler400 = 'errorPage.views.my_custom_bad_request_view'