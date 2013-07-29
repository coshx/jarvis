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
        weatherData_temp_avg = json.loads(weatherData)['list'][0]['main']['temp']
        weatherData_weather_desc = json.loads(weatherData)['list'][0]['weather'][0]['description']
        response_data = {'command':'speak','data':'It is ' + str(weatherData_temp_avg) + ' degrees outside with ' + str(weatherData_weather_desc) + "."}
    elif extractedCommand["command"] == "temperature":
        weatherData = urllib2.urlopen("http://api.openweathermap.org/data/2.5/find?q=Boulder,co&units=imperial").read()
        weatherData_temp_avg = json.loads(weatherData)['list'][0]['main']['temp']
        weatherData_temp_high = json.loads(weatherData)['list'][0]['main']['temp_max']
        weatherData_temp_low = json.loads(weatherData)['list'][0]['main']['temp_min']
        response_data = {'command':'speak','data':'It is ' + str(weatherData_temp_avg) + ' degrees outside with a high of '+str(weatherData_temp_high)+' degrees and a low of '+str(weatherData_temp_low) + ' degrees.'}
    elif extractedCommand['command'] == "wind":
        weatherData = urllib2.urlopen("http://api.openweathermap.org/data/2.5/find?q=Boulder,co&units=imperial").read()
        weatherData_wind_speed = json.loads(weatherData)['list'][0]['wind']['speed']
        weatherData_wind_heading = json.loads(weatherData)['list'][0]['wind']['deg']
        response_data = {'command':'speak','data':'The wind speed is currently ' + str(weatherData_wind_speed) + " miles per hour with heading " + str(weatherData_wind_heading) + "."}
    elif extractedCommand['command'] == "play":
        youtubeData = urllib2.urlopen('https://www.googleapis.com/youtube/v3/search?q='+extractedCommand['data']+'&key=AIzaSyBL6aPKYByygs9oHB5rStYhTBKtklqRkrI&part=snippet').read()
        youtubeData_url = json.loads(youtubeData)['items'][0]['id']['videoId'];
        response_data = {'command':'playerAction','data': ['play', youtubeData_url]}
    elif extractedCommand["command"] == "pause":
        response_data = {'command':'playerAction','data':"pause"}
    elif extractedCommand["command"] == "resume":
        response_data = {'command':'playerAction','data':"resume"}
    elif extracteCommand['command'] == "volume":
        response_data = {'command':'playerAction','data': ['volume',extractedCommand['data']]}
    elif extractedCommand["command"] == "ask":
        response_data = {'command':'speak','data':extractedCommand["data"]}
    else:
        response_data = {'command':'speak','data':'That command is not yet avaliable or was stated in a way I do not understand'}
    return HttpResponse(simplejson.dumps(response_data), content_type="application/json") 