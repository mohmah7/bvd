from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('ci_monitor.pull.views',
    
    url(r'^$', 'home',name='home'),
	url(r'^get_jenkins_views/$','poll_jenkins_servers',name='poll_jenkins_view'),
	
	
	
)