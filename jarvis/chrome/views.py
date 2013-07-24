from django.http import HttpResponse
from django.template import RequestContext, loader

def home(request):
    template = loader.get_template('chrome/index.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))