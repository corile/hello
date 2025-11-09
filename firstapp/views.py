from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

from firstapp.forms import ReservationForm 

# Create your views here.
def hello_world(request):
    return HttpResponse("Hello, world!")

class HelloWorldView(View):
    def get(self, request):
        return HttpResponse("Hello from Class-Based View!")
    
def home(request):
    form = ReservationForm()

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Reservation created successfully!")

    # Template lives at firstapp/templates/index.html, so the correct
    # template name (with APP_DIRS enabled) is just 'index.html'.
    return render(request, 'index.html', {'form': form})