from django import forms
import pyotp
from django.contrib.auth.models import User
from server.models import Organization, Client, UserProfile, Sensor, \
    ClientRequest
from _socket import timeout

class OrganizationForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
                           help_text="Please enter the organization name.")
    
    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Organization
        fields = ('name',)
        
class SensorForm(forms.ModelForm):
    def __init__(self, uuid, *args, **kwargs):
        super(SensorForm, self).__init__(*args, **kwargs)

        self.fields['uuid'] =  forms.CharField(max_length=128,
                                    help_text="Uuid*",
                                    initial=uuid)
        
    command = forms.ChoiceField(Sensor.COMMANDS, help_text="Command", required=True)
    
    description = forms.CharField(max_length=128,
                                  help_text="Description for the sensor*")
    privacy = forms.ChoiceField(Sensor.PRIVACY, help_text="Privacy", required=False)
    
    protocol_name = forms.CharField(max_length=128, help_text="Protocol name*")
    protocol_min = forms.IntegerField(help_text="Min value variation*")
    protocol_max = forms.IntegerField(help_text="Max value variation*")
    meas_unit = forms.CharField(max_length=20, help_text="Unit of measure*")
    
    
    sampling_type = forms.ChoiceField(Sensor.EMPTY_FIELD + list(Sensor.SAMPLING_TYPES),
                                      help_text="Sampling Type*")
    

    period = forms.IntegerField(help_text="Sampling period*", required=False)
    period_unit = forms.ChoiceField(Sensor.UNIT_TYPE,
                                     help_text="Measuring unit*",
                                     required=False)
    
    delta = forms.IntegerField(help_text="Delta value*", required=False)
    delta_type = forms.ChoiceField(Sensor.DELTA_TYPE,
                                   help_text="Delta type*", initial=None,
                                   required=False)
    delta_min = forms.IntegerField(help_text="Min delta variation", required=False)
    delta_max = forms.IntegerField(help_text="Max delta variation", required=False)
    timeout = forms.IntegerField(help_text="Timeout for delta samplig", required=False)
    timeout_unit = forms.ChoiceField(Sensor.EMPTY_FIELD + list(Sensor.UNIT_TYPE),
                                     help_text="Choose second or millisecond, otherwise will be ignored", required=False)
    
    sending_type = forms.ChoiceField(Sensor.EMPTY_FIELD + list(Sensor.SENDING_TYPES),
                                     help_text="Sending Type*")
    
    quota = forms.IntegerField(help_text="Quota in Kb or Mb*", required=False)
    
    quota_unit = forms.ChoiceField(Sensor.EMPTY_FIELD + list(Sensor.QUOTA_UNIT),
                                     help_text="Quota unit*", required=False)
    
    
    class Meta:
        model = Sensor
        
#         deviceId = sensor.uuid
#                 description = sensor.description
#                 privacy = sensor.privacy
#                 sensor.sampling_type
#                 sensor.period
#                 sensor.period_unit
#                 sensor.protocol_name
#                 sensor.protocol_min
#                 sensor.protocol_max
        
        fields = ('command', 'description', 'protocol_name',
                  'protocol_min', 'protocol_max', 'meas_unit', 'privacy','sampling_type',
                  'period' , 'period_unit', 'delta_type', 'delta_min', 'delta_max', 'timeout', 'timeout_unit', 'sending_type', 'quota', 'quota_unit',)

    def clean(self):
        super(SensorForm, self).clean()
        return self.cleaned_data

class ClientForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ClientForm, self).__init__(*args, **kwargs)
        user_profile = UserProfile.objects.get(user=User.objects.get(username=self.user))
        self.myorg = user_profile.organizations
        
        self.fields['client'] = forms.ModelChoiceField(
                        queryset=ClientRequest.objects.filter(organization__iexact=self.myorg.name),
                        help_text="Choose pending clients")

    class Meta:
        # Provide an association between the ModelForm and a model
        model = ClientRequest

        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them...
        # Here, we are hiding the foreign key.
        # we can either exclude the category field from the form,
        fields = ()
        # or specify the fields to include (i.e. not include the category field)
        # fields = ('title', 'url', 'views')
        
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
        
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('organizations',)

        
