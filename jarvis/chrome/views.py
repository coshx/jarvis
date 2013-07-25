from django.http import HttpResponse
from django.template import RequestContext, loader
from django.utils import simplejson
import json, urllib2

def home(request):
  template = loader.get_template('chrome/index.html')
  context = RequestContext(request)
  return HttpResponse(template.render(context))

def process_command(request):
    # lots of real logic needed here. Stuff is going to need to be extracted from here eventually...
    requested_service = request.GET['q']
    if requested_service == "weather":
        weatherData = urllib2.urlopen("http://api.openweathermap.org/data/2.5/find?q=Boulder,co&units=imperial").read()
        weatherData_temp = json.loads(weatherData)['list'][0]['main']['temp']
        response_data = {'response': 'It is ' + str(weatherData_temp) + ' degrees outside'}
    else:
        response_data = {'response': request.GET}
    return HttpResponse(simplejson.dumps(response_data), content_type="application/json") 