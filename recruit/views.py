from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.utils import timezone
from recruit.models import Room

def index(request):
    return render_to_response('recruit/index.html', {}, context_instance=RequestContext(request))

def create(request):
    try:
        type = request.POST['type']
        creator = request.POST['creator']
        if not creator: raise KeyError
        comment = request.POST['comment']
        room = Room(type=type,
                    createdate=timezone.now(),
                    comment=comment)
    except (KeyError):
        return render_to_response('recruit/index.html', {
            'error_message': "invalid parameters"}, context_instance=RequestContext(request))
    else:
        room.save()
        room.user_set.create(name=creator, is_creator=True)
        return HttpResponseRedirect(reverse('recruit.views.room', args=(room.id,)))
        
def room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    return render_to_response('recruit/room.html',{
        'room': room,
    }, context_instance=RequestContext(request))

def join(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    try:
        name = request.POST['name']
        if not name: raise KeyError
    except (KeyError):
        return render_to_response('recruit/room.html', {
            'room': room,
            'error_message': "invalid name"
        }, context_instance=RequestContext(request))
    else:
        if room.is_full():
            return render_to_response('recruit/room.html', {
                'room': room,
                'error_message': "invalid operation"
            }, context_instance=RequestContext(request))
        room.user_set.create(name=name, is_creator=False)
        return HttpResponseRedirect(reverse('recruit.views.room', args=(room.id,)))
