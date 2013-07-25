from django.http import HttpResponse
from django.template import RequestContext, loader
from django.utils import simplejson
import json, urllib2
from chrome.models import CommandProcessor

def home(request):
  template = loader.get_template('chrome/index.html')
  context = RequestContext(request)
  return HttpResponse(template.render(context))
  
def textToSpeechTest(request):
    template = loader.get_template('chrome/texttospeech_test.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def process_command(request):
    # lots of real logic needed here. Stuff is going to need to be extracted from here eventually...
    input = request.GET['q'].lstrip()

    if not CommandProcessor.isCommand(input):
        print input + " is not a command"
        return HttpResponse({}, content_type="application/json")

    extractedCommand = CommandProcessor.extractCommand(input)
    print extractedCommand
    if extractedCommand["command"] == "weather":
        weatherData = urllib2.urlopen("http://api.openweathermap.org/data/2.5/find?q=Boulder,co&units=imperial").read()
        weatherData_temp = json.loads(weatherData)['list'][0]['main']['temp']
        response_data = {'speak': 'It is ' + str(weatherData_temp) + ' degrees outside'}
    else:
        response_data = {'speak': 'That command is not yet avaliable or was stated in a way I do not understand'}
    return HttpResponse(simplejson.dumps(response_data), content_type="application/json") 