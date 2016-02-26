'''
Created on 26/mag/2015

@author: koelio
'''

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.org_list),
]

urlpatterns = [
    url(r'^$', views.org_list),

    url(r'^myclients/$', views.client_list),

    url(r'^add_org/$', views.add_org, name='add_org'),
    url(r'^add_client/$', views.add_client_org, name='add_client_org'),

    #url(r'^added_client/$', views.client_list, name='added_client_org'),

    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),

    url(r'^client_list/', views.client_list, name='client_list'),
    url(r'^sensor_list/', views.sensor_list, name='sensor_list'),

    #non mettere mai sopra cliet_list perche il fetch e lineare
    url(r'^(?P<client_id>.*)/add_sensor$', views.add_sensor, name='add_sensor'),
    url(r'^(?P<client_id>.*)/$', views.my_client, name='my_client'),
    url(r'^(?P<client_id>.*)/graph$', views.show_graph, name='show_graph'),

    url(r'^(?P<sensor_id>.*)/sensor$', views.my_sensor, name='my_sensor'),
    #url(r'^add_sensor/$', views.add_sensor, name='add_sensor'),
    url(r'^(?P<client_id>.*)/remove_client$', views.remove_client, name='remove_client'),
    url(r'^(?P<sensor_id>.*)/remove_sensor$', views.remove_sensor, name='remove_sensor'),

]
