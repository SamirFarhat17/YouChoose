from django.shortcuts import render, redirect
from .models import Video
from .forms import VideoForm
from django.views.generic import TemplateView

# Create your views here.
def vidlist(request):
    return render(request, 'channel/vidlist.html')


class HomeView(TemplateView):
    template_name = 'channel/home.html'

    def get(self, request):
        form  = VideoForm()
        return render(request, self.template_name, {'form' : form})

    def post(self, request):
        form = VideoForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect('vidlist')
