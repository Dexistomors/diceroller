from dmroller.models import RollConfig, RoomUser, RollResult, Room
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import loader
import json
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

@login_required
def room(request):
    if request.method == 'GET':
        if not request.GET:
            #to get all rooms for this user
            room_codes = [r.room.room_code for r in RoomUser.objects.filter(user=request.user)]
            resp = {'data': room_codes}
            return HttpResponse(json.dumps(resp, indent=4))   
        elif 'room_code' in request.GET:
            #get all rollresults and configs for this room code
            try:
                room = Room.objects.get(room_code=request.GET.get('room_code'))
            except Room.DoesNotExist:
                return HttpResponse(json.dumps({'error': {'code': 404, 'message': 'No rooms found'}}))
            resp = {'data': []}
            for roll_result in RollResult.objects.filter(room=room):
                tmp = {}
                tmp['date'] = str(roll_result.date)
                tmp['user'] = roll_result.user.username
                tmp['roll_result'] = json.loads(roll_result.roll_result)
                tmp['roll_config'] = json.loads(roll_result.roll_config.roll_config)
                resp['data'].append(tmp)
            return HttpResponse(json.dumps(resp, indent=4))
        return HttpResponse(json.dumps({'error': {'code': 404, 'message': 'Bad Request'}}))
    
    elif request.method == 'PUT':
        #create a room and return room code
        
        pass

    elif request.method == 'POST':
        #add a user to this room with a room code
        pass
    #return error page
    
        
