from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from server.models import UserProfile, Organization, Sensor, Client, Measurement
from server.forms import SensorForm

from serv2.JsonForGraph import JsonForGraph


BASE_URL = 'remsens'

def index(request):
    user = request.user
    if user.is_authenticated():
        return redirect('client_list')
    else:
        return render(request, BASE_URL + '/index.html')
 
def user_list(request):
    users = UserProfile.objects.all();
    context = {'users': users}
    return render(request, BASE_URL + '/', context)
 
@login_required
def client_list(request):

    user = UserProfile.objects.get(user=request.user)
    # Organization.objects.get(name=organization_name)
    
    myorg = user.organizations
    clients = Client.objects.all();   
    context = {'clients': clients, 'myorg': myorg, 'user1': user, }
    return render(request, BASE_URL + '/client_list.html', context)

@login_required
def sensor_list(request):
    sensors = Sensor.objects.all()
    context = {'sensors': sensors}
    return render(request, BASE_URL + '/sensor_list.html', context)

 
def org_list(request):
    orgs = Organization.objects.all();
    context = {'orgs': orgs}
    return render(request, BASE_URL + '/index.html' , context)

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")


@login_required
def my_client(request, client_id):
    try:
        client = Client.objects.get(uuid=client_id)
        user = UserProfile.objects.get(user=request.user)
        myorg = user.organizations
        
        context = {'client': client, 'myorg': myorg, 'user1':user, }
        return render(request, BASE_URL + '/client.html', context)
        
        
    except ObjectDoesNotExist:
        return HttpResponse("<h1>The metering point with this uuid doesn't exist. ")
    
@login_required
def my_sensor(request, sensor_id):
    
    if request.method == 'POST':
        
        if request.POST.get('delete_pressed'):
            
            meas_list = request.POST.getlist('meas')
            
            # deleting character T in the timestamp to match the format of filtering option
            for i, meas in enumerate(meas_list):
                
                s = list(meas)
                del s[0]
                del s[26]
                s[10] = ' '
                meas = "".join(s)
                meas_list[i] = meas
            
            selected = Measurement.objects.filter(pk__in=meas_list)
            selected.delete()
    else:
        pass        
        
    try:
        sensor = Sensor.objects.get(uuid=sensor_id)
        client = sensor.client
        user = UserProfile.objects.get(user=request.user)
        myorg = user.organizations
        
        initial_vals = sensor.__dict__
        
        sensor_form = SensorForm(sensor_id, initial=initial_vals)
        
        context = {'client': client, 'sensor': sensor, 'myorg': myorg, 'user1':user, 'form':sensor_form, }
        return render(request, BASE_URL + '/sensor.html', context)
        
        
    except ObjectDoesNotExist:
        return HttpResponse("<h1>The sensor with this uuid doesn't exist. ")
        
    
def show_graph(request, client_id):
    
    client = Client.objects.get(uuid=client_id)
    user = UserProfile.objects.get(user=request.user)
    org = user.organizations
    
    context = {'client':client, 'myorg': org}
    
    jsonGr = JsonForGraph()
    jsonGr.composeJson(client_id)
#     stime.sleep(3)
    return render(request, BASE_URL + '/graph.html', context)