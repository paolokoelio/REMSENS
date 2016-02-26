from django.shortcuts import render, redirect, get_object_or_404
from django.db import  IntegrityError
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from server.models import UserProfile, Sensor, Client, ClientRequest
from server.forms import OrganizationForm, ClientForm, SensorForm
from server.views.readingObjects import client_list

import uuid
from serv2.utils import conf_updater

BASE_URL = 'remsens'

###################### DYNAMIC ACTIONS ###################

def add_org(request):
    if request.method == 'POST':
        form = OrganizationForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new org to the database.
            form.save(commit=True)

            # Now call the page view.
            # The user will be shown the homepage (server/).
            return client_list(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print(form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        form = OrganizationForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, BASE_URL + '/add_org.html', {'form': form})

@login_required
def add_sensor(request, client_id):
    
    client = Client.objects.get(uuid=client_id)
    user = UserProfile.objects.get(user=request.user)
    myorg = user.organizations
    
    if request.method == 'POST':
        sensor_form = SensorForm(request.user, request.POST)
        
        
        if  sensor_form.is_valid():
            
            uuid_dev = sensor_form.cleaned_data['uuid']
            desc = sensor_form.cleaned_data['description']
            
            try:
                new_sensor = Sensor.objects.get(uuid=uuid_dev)
            except Sensor.DoesNotExist:
                try:
                    new_sensor = Sensor.objects.create(uuid=uuid_dev,
                                                       description=desc,
                                                       client=client)
                except IntegrityError:
                    # printing traceback for testing purposes
                    print(sensor_form.errors)
                    import traceback
                    tmp = traceback.format_exc()

                    return HttpResponse("<b>" + str(client.uuid) + "</b>" + " " + str(tmp))
            
            new_sensor.protocol_name = sensor_form.cleaned_data['protocol_name']
            new_sensor.protocol_min = sensor_form.cleaned_data['protocol_min']
            new_sensor.protocol_max = sensor_form.cleaned_data['protocol_max']
            new_sensor.command = sensor_form.cleaned_data['command']
            new_sensor.meas_unit = sensor_form.cleaned_data['meas_unit']
            new_sensor.privacy = sensor_form.cleaned_data['privacy']
            new_sensor.sampling_type = sensor_form.cleaned_data['sampling_type']
            new_sensor.sending_type = sensor_form.cleaned_data['sending_type']
            
            
            if sensor_form.cleaned_data['sampling_type'] == 'PERIODIC':
                new_sensor.period = sensor_form.cleaned_data['period']
                new_sensor.period_unit = sensor_form.cleaned_data['period_unit']
                new_sensor.delta_type = None
                new_sensor.save()
            elif sensor_form.cleaned_data['sampling_type'] == 'APERIODIC':
                new_sensor.delta = sensor_form.cleaned_data['delta']
                new_sensor.delta_type = sensor_form.cleaned_data['delta_type']
                new_sensor.delta_min = sensor_form.cleaned_data['delta_min']
                new_sensor.delta_max = sensor_form.cleaned_data['delta_max']
                new_sensor.timeout = sensor_form.cleaned_data['timeout']
                new_sensor.timeout_unit = sensor_form.cleaned_data['timeout_unit']
                
                # needed because the client won't accept a null
                new_sensor.period = 1
                new_sensor.period_unit = 'sec'
                new_sensor.save()
            else:
                pass
            
            if sensor_form.cleaned_data['sending_type'] == 'BATCH':
                new_sensor.quota = sensor_form.cleaned_data['quota']
                new_sensor.quota_unit = sensor_form.cleaned_data['quota_unit']
                new_sensor.save()
            else:
                pass
            
            new_sensor.save()                
            
            new_sensor.fields = dict((field.name, field.value_to_string(new_sensor))
                                            for field in new_sensor._meta.fields)
            
            
            # update flag in Server.conf_handler in order to permit delivery to the client
            conf_updater.setFlag1(True)
            
            
            
            context = {'client': client, 'user1': user, 'myorg':myorg, 'sensor':new_sensor, }
            
            # delete function in case of command "cancel"
            if new_sensor.command == Sensor.DELETE:
                remove_sensor(request, new_sensor.uuid)
            
            
            return render(request,
                      BASE_URL + '/added_sensor.html', context)
        
                                    
        else:
            print(sensor_form.errors)
            # return HttpResponse("<h1>Form not valid, go back and retry.</h1></br>" + str(sensor_form.errors))
    else:
    
        sensor_form = SensorForm(uuid.uuid4())

    context = {'client': client, 'user1': user, 'myorg':myorg, 'form':sensor_form, }
    return render(request, 'remsens/add_sensor.html', context)

@login_required
def add_client_org(request):
    user = UserProfile.objects.get(user=request.user)
    myorg = user.organizations
    err = False
    succ = False

    if request.method == 'POST':
        choice_form = ClientForm(request.user, request.POST)

        if choice_form.is_valid():
            uuid = choice_form.cleaned_data['client'].uuid
            name = choice_form.cleaned_data['client'].name
            try:
                new_client = Client.objects.create(uuid=uuid, name=name, organizations=myorg, is_enabled=True)
                new_client.save()
                succ = True
                
                # to check
                ClientRequest.objects.get(uuid=uuid).delete()
                return render(request, 'remsens/add_client.html',
                              {'user1': user, 'myorg':myorg, 'client':new_client, 'succ': succ, })
            except IntegrityError:
                print(choice_form.errors)
                err = True
                # request.method = 'GET'
                # return add_client_org(request)
                return render(request, 'remsens/add_client.html',
                              {'choice_form': choice_form, 'user1': user, 'myorg':myorg, 'err': err, 'uuid':uuid, })
            
        else:
            print(choice_form.errors)
    else:
        
        choice_form = ClientForm(user)
    
    context = {'choice_form': choice_form, 'user1': user, 'myorg':myorg, }
    return render(request, BASE_URL + '/add_client.html', context)

@login_required
def remove_client(request, client_id):
        
    client = get_object_or_404(Client, uuid=client_id)
    client.delete()
    return redirect('/')
    
@login_required
def remove_sensor(request, sensor_id):

    sensor = get_object_or_404(Sensor, pk=sensor_id)
    sensor.delete()
    return redirect('/')
