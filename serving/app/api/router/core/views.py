import json
from time import sleep, time

from django.shortcuts import redirect, render

from user.utility import login_required


# @login_required
def home(request):
    return render(request, "ws_test.html")
