from dmroller.models import RollConfig
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import loader
import diceroller

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render(None, request))

def login(request):
    template = loader.get_template('registration/login.html')
    return HttpResponse(template.render(None, request))

@login_required
def api_roll(request):
    data = request.POST.get("roll_config")
    try:
        roll = diceroller.Roll.deserialize(data)
        result = 'Dice result: {}'.format(roll.roll().serialize())
    except Exception as error:
        result = 'Encountered an error {}'.format(error)
        
    return HttpResponse("Result: {}".format(result))

@login_required
def roller(request):
    context = dict()
    context['rollconfigs'] = RollConfig.objects.filter(user=request.user).iterator()
    template = loader.get_template('roller.html')
    return HttpResponse(template.render(context, request))