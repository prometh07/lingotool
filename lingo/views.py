from django.http import HttpResponse

def register(request):
   return HttpResponse("register") 


def new_set(request):
   return HttpResponse("new_set") 
