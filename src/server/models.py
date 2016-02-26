from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.dateformat import format


class Organization(models.Model):
    name = models.CharField(max_length=128, unique=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
   
    def __str__(self):
        return str(self.name)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    created_date = models.DateTimeField(default=timezone.now)
    organizations = models.ForeignKey(Organization, null=True)
    
    def __str__(self):
        return self.user.username
    
class Client(models.Model):
    uuid = models.CharField(max_length=200, unique=True, primary_key=True)
    name = models.CharField(max_length=200)
    organizations = models.ForeignKey(Organization, null=True)
    latitude = models.IntegerField(null=True, blank=True, default=None)
    longitude = models.IntegerField(null=True, blank=True, default=None)
    place_name = models.CharField(max_length=200, blank=True)
    is_enabled = models.BooleanField(default=False)
    starting_date = models.DateTimeField(blank=True, null=True, default=timezone.now)
    
    def __str__(self):
        return str(self.name + " - " + self.organizations.name)
      
class Sensor(models.Model):
    # useful to stay DRY
    NONE = ''
    EMPTY_FIELD = [(NONE, 'select')]
    
    PUBLIC = 'public'
    PRIVATE = 'private'
    
    ENABLE = 'enable'
    DISABLE = 'disable'
    DELETE = 'cancel'
    
    PERIODIC = 'PERIODIC'
    APERIODIC = 'APERIODIC'
    INSTANT = 'INSTANT'
    BATCH = 'BATCH'
    
    SEC = 'sec'
    MSEC = 'msec'
    MIN = 'min'
    HOUR = 'h'
    
    ABSOLUTE = 'absolute'
    RELATIVE = 'relative'
    
    COMMANDS = (
                (ENABLE, 'Enable'),
                (DISABLE, 'Disable'),
                (DELETE, 'Delete'))
    PRIVACY = (
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'))
    
    SENDING_TYPES = (
        (INSTANT, 'Instant'),
        (BATCH, 'Batch'))
    
    QUOTA_UNIT = (
              ('kb', 'Kb'),
              ('mb', 'Mb'),
              ('samples', 'samples'))
    
    SAMPLING_TYPES = (
        (PERIODIC, 'Periodic'),
        (APERIODIC, 'Aperiodic'),
    )
    
    UNIT_TYPE = (
        (SEC, 'second'),
        (MSEC, 'millisecond'),
        (MIN, 'minute'),
        (HOUR, 'hour'),)
    
    DELTA_TYPE = (
        (ABSOLUTE, 'Absolute'),
        (RELATIVE, 'Relative'),)
    
    description = models.CharField(max_length=200, blank=True)
    uuid = models.CharField(max_length=200, unique=True, primary_key=True)
    client = models.ForeignKey(Client, null=True)
    starting_date = models.DateTimeField(blank=True, null=True, default=timezone.now)
    
    
    command = models.CharField(max_length=8,choices=COMMANDS,default=ENABLE)
    
    protocol_name = models.CharField(max_length=50, default='', null=True)
    protocol_min = models.SmallIntegerField(null=True, blank=True, default=None)
    protocol_max = models.SmallIntegerField(null=True, blank=True, default=None)
    meas_unit = models.CharField(max_length=20, default='', null=True)
     
    privacy = models.CharField(max_length=7,choices=PRIVACY,default=PUBLIC)
    
    quota = models.IntegerField(null=True, blank=True, default=None)
    quota_unit = models.CharField(max_length=10,choices=QUOTA_UNIT,default=None, null=True)
    
    sending_type = models.CharField(max_length=10,choices=SENDING_TYPES,default=INSTANT)     
    sampling_type = models.CharField(max_length=10,
                                      choices=SAMPLING_TYPES, default=PERIODIC)
    # Case periodic sampling:   
    period = models.SmallIntegerField(null=True, blank=True, default=None)
    period_unit = models.CharField(max_length=4,choices=UNIT_TYPE,
                                      default=None, blank=True, null=True)
    # Case aperiodic sampling
    delta = models.SmallIntegerField(null=True, blank=True, default=None) 
    delta_type = models.CharField(max_length=8,choices=DELTA_TYPE,
                            default=None, blank=True, null=True)
    
    delta_min = models.SmallIntegerField(null=True, blank=True, default=None)
    delta_max = models.SmallIntegerField(null=True, blank=True, default=None)
    timeout = models.SmallIntegerField(null=True, blank=True, default=None)
    timeout_unit = models.CharField(max_length=4,choices=UNIT_TYPE,
                                      default=None, blank=True, null=True)

    def start_date(self):
        self.starting_date = timezone.now()
        self.save()
      
    def __str__(self):
        return str(self.description + " " + self.uuid)

class Measurement(models.Model):
    timestamp = models.DateTimeField(primary_key=True, unique=True);
    type = models.CharField(max_length=200, blank=True)
    value = models.IntegerField(null=True, blank=True, default=None);
    error = models.CharField(max_length=200, null=True, blank=True, default=None);
    sensor = models.ForeignKey(Sensor, null=True)
    
    def __str__(self):
        time = str(format(self.timestamp, 'c'))
        time_tr = time[:19] if len(time) > 18 else time
        
        if self.value != None:
            val = self.value
        else:
            val = self.error
    
        return str(str(time_tr)) + ": " + str(val) + " - " + self.sensor.description
    def timestamp_set(self):
        return self.timestamp_set.all()
    
class ClientRequest(models.Model):
    uuid = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    token = models.IntegerField(null=True)
    desc = models.CharField(max_length=400, default=None, null=True)
    
#     def requestsByOrg(self, org):
#         self.organization.get_c
      
    def __str__(self):
        tmp = self.name + " " + str(self.token)
        return tmp
#     def uuid(self):
#         return self.uuid
#     def name(self):
#         return self.name

# class Zero(models.Model):
#     message = models.TextField()
#     
#     objects = Zero_Manager()
# 
#     def __str__(self):
#         return self.message
