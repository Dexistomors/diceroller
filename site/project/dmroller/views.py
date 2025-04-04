from dmroller.models import RollConfig, RoomUser, RollResult, Room
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import loader
from datetime import datetime
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
    roll_config_json = request.POST.get("roll_config")
    try:
        roll_config = diceroller.RollConfig.deserialize(roll_config_json)
        roll = diceroller.RollConfig.create_roll(roll_config)
        result = roll.roll().serialize()
        prettify = roll.prettify() + '=' + str(roll.final_value)
    except Exception as error:
        return HttpResponse(json.dumps({'error': {'code': 404, 'message': 'Could not parse roll_config %s' % error}}))
    
    if 'room_code' in request.POST and request.POST.get('room_code') and not request.POST.get('room_code') == 'N/A':
        room_code = request.POST.get('room_code')
        try:            
            room = Room.objects.get(room_code=room_code)
        except Room.DoesNotExist:
            return HttpResponse(json.dumps({'error': {'code': 404, 'message': 'No rooms found'}}))
        
        roll_config = RollConfig(user=request.user, roll_config=roll_config_json)
        roll_config.save()
        roll_result = RollResult(user=request.user, room=room, roll_config=roll_config, roll_result=result, prettify=prettify)
        roll_result.save()
    return HttpResponse("Result: {}".format(result))

@login_required
def roller(request):
    context = dict()
    context['rollconfigs'] = RollConfig.objects.filter(user=request.user, name__isnull=False).iterator()
    context['roomlist'] = RoomUser.objects.filter(user=request.user).iterator()
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
        
        elif 'room_code' in request.GET and 'users' in request.GET:
            try:
                room = Room.objects.get(room_code=request.GET.get('room_code'))
            except Room.DoesNotExist:
                return HttpResponse(json.dumps({'error': {'code': 404, 'message': 'No rooms found'}}))
            room_users = [r.user.username for r in RoomUser.objects.filter(room=room)]
            resp = {'data': room_users}
            return HttpResponse(json.dumps(resp, indent=4))        

        elif 'room_code' in request.GET:
            #get all rollresults and configs for this room code
            try:
                room = Room.objects.get(room_code=request.GET.get('room_code'))
            except Room.DoesNotExist:
                return HttpResponse(json.dumps({'error': {'code': 404, 'message': 'No rooms found'}}))
            resp = {'data': {'users': [], 'roll_results': []}}
            if 'date' in request.GET:
                #get all objects after this date
                date = datetime.fromisoformat(request.GET.get('date'))
                roll_results = RollResult.objects.filter(room=room, date__gt=date).order_by('date')
            else:
                #get all objects
                roll_results = RollResult.objects.filter(room=room).order_by('date')
            for roll_result in roll_results:
                tmp = {}
                tmp['date'] = str(roll_result.date)
                tmp['user'] = roll_result.user.username
                tmp['roll_result'] = json.loads(roll_result.roll_result)
                tmp['roll_config'] = json.loads(roll_result.roll_config.roll_config)
                tmp['prettify'] = roll_result.prettify
                resp['data']['roll_results'].append(tmp)
            room_users = [r.user.username for r in RoomUser.objects.filter(room=room)]
            resp['data']['users'] = room_users
            return HttpResponse(json.dumps(resp, indent=4))
        return HttpResponse(json.dumps({'error': {'code': 404, 'message': 'Bad Request'}}))
    
    elif request.method == 'POST':
        #add a user to this room with a room code
        if 'room_code' in request.POST:
            #create room if not exists and add current user
            try:
                room = Room.objects.get(room_code=request.POST.get('room_code'))
            except Room.DoesNotExist:
                room = Room(room_code=request.POST.get('room_code'))
                room.save()
            try:
                RoomUser.objects.get(room=room, user=request.user)
            except RoomUser.DoesNotExist:
                room_user = RoomUser(user=request.user, room=room)
                room_user.save()
            return HttpResponse(json.dumps({'data': 'success'}))
        return HttpResponse(json.dumps({'error': {'code': 404, 'message': 'Bad Request'}}))
    

@login_required
def api_rollconfig(request):
    if request.method == 'GET':
        #TODO: return JSON with all roll_configs for current user
        if not request.GET:
            roll_configs = [r.roll_config for r in RollConfig.objects.filter(user=request.user)]
            resp = {'data': roll_configs}
            return HttpResponse(json.dumps(resp, indent=4))
    elif request.method == 'POST':        
        try:
            roll_config = request.POST.get("roll_config")
            roll_name = request.POST.get("roll_name")
            #TODO: Filter through existing roll_config objects, if roll_name exists, replace
            # that object's roll_config

            #roll_config_list = RollConfig.objects.filter(user=request.user)                
            roll_config_test = diceroller.RollConfig.deserialize(roll_config)
            roll_config_serialized = roll_config_test.serialize()
            #for roll_config_object in roll_config_list:
            #    if roll_config_object.name == roll_name:
            #        roll_config_object.roll_config = roll_config_serialized
            #        roll_config_object.save()
            roll_config_save = RollConfig(user=request.user, roll_config=roll_config_serialized, name=roll_name)
            roll_config_save.save()
            return HttpResponse(json.dumps({'data': 'success'}))            
        except Exception as error:
            return HttpResponse(json.dumps({'error': {'code': 404, 'message': 'Could not parse roll_config for save %s' % error}}))
        #TODO: take in POST data that includes roll_config and save to database under current user
        #TODO: Then return all roll_configs for current user
        pass
    elif request.method == 'DELETE':
        #TODO: take in name of roll_config and delete from database, then return roll_config for current user
        pass
    return HttpResponse(json.dumps({'error': {'code': 404, 'message': 'Bad Request'}}))