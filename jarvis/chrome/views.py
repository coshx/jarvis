from django.http import HttpResponse
from django.template import RequestContext, loader
from django.utils import simplejson

def home(request):
  template = loader.get_template('chrome/index.html')
  context = RequestContext(request)
  return HttpResponse(template.render(context))

def process_command(request):
  # lots of real logic needed here. Stuff is going to need to be extracted from here eventually...
  response_data = {'response': 'It is 88 degrees outside'}
  return HttpResponse(simplejson.dumps(response_data), content_type="application/json") 