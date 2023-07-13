from django.shortcuts import render
from django.contrib.auth.decorators import login_required



@login_required
def Base(request):

    return render(
        request,
        'index/base.html',
    )