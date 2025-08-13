from dmroller.models import User_RollConfig, RoomUser, RollResult, Room
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
        
        roll_config = User_RollConfig(user=request.user, roll_config=roll_config_json)
        roll_config.save()
        roll_result = RollResult(user=request.user, room=room, roll_config=roll_config, roll_result=result, prettify=prettify)
        roll_result.save()
    return HttpResponse("Result: {}".format(result))

@login_required
def roller(request):
    context = dict()
    context['user_rollconfigs'] = User_RollConfig.objects.filter(user=request.user, name__isnull=False).iterator()
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
        if not request.GET:
            roll_configs = User_RollConfig.objects.filter(user=request.user)
            user_config_list = []
            for user_single_config in roll_configs:
                _user_config = {}
                _user_config["name"] = user_single_config.name
                _user_config["rollconfig"] = user_single_config.roll_config
                user_config_list.append(_user_config)
            resp = {'data': user_config_list}
            return HttpResponse(json.dumps(resp, indent=4))
    elif request.method == 'POST':
        # Taking in a configuration, checking over the existing RollConfig objects, 
        # and either creating new, overwriting, or deleting objects accordingly.
        try:
            roll_config = request.POST.get("roll_config")
            roll_name = request.POST.get("roll_name")
            config_delete_request = request.POST.get("marked_for_deletion")
            roll_config_list = User_RollConfig.objects.filter(user=request.user)               
            new_roll_config_object = diceroller.RollConfig.deserialize(roll_config)
            serialized_roll_config = new_roll_config_object.serialize()
            for roll_config_object in roll_config_list:
                if roll_config_object.name == roll_name and config_delete_request == 'true':
                    roll_config_object.delete()
                    return HttpResponse(json.dumps({'data': 'success'}))
                elif roll_config_object.name == roll_name:
                    old_roll_config_object = roll_config_object
                    new_roll_config_object.roll_config = serialized_roll_config
                    old_name_new_config = diceroller.RollConfig.set_config(old_roll_config_object, new_roll_config_object)
                    old_name_new_config.save()
                    return HttpResponse(json.dumps({'data': 'success'}))
            roll_config_save = User_RollConfig(user=request.user, name=roll_name, roll_config=serialized_roll_config)
            roll_config_save.save()
            return HttpResponse(json.dumps({'data': 'success'}))            
        except Exception as error:
            return HttpResponse(json.dumps({'error': {'code': 404, 'message': 'Could not parse roll_config for save %s' % error}}))
    return HttpResponse(json.dumps({'error': {'code': 404, 'message': 'Bad Request'}}))