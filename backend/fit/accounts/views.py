import json

from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.http import HttpResponseForbidden

from fit.accounts.forms import LoginForm


@csrf_exempt
def login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']		
        form = LoginForm(data={"username": username, "password": password})
        if form.is_valid():
            user = authenticate(username=form.data['username'], password=form.data['password'])
            data = serializers.serialize("json", user)
            return HttpResponse(data, content_type='application/json')
        else:
            return HttpResponseForbidden()
