from django.shortcuts import render, redirect
from .models import Channel
from .forms import ChannelForm
from .lib.retrieve import get_videos
from django.views.generic import TemplateView
from django.views.generic import (
    DetailView
)
from .lib.MachineLearn import train
from .lib.analysis import analyze

# Create your views here.
def vidlist(request):
    return render(request, 'channel/vidlist.html')


class HomeView(TemplateView):
    global model
    model = train()
    def get(self, request):
        form  = ChannelForm()
        return render(request, 'channel/boot.html', {'form' : form})

    def post(self, request):
        form = ChannelForm(request.POST)
        if form.is_valid():
            link = form.cleaned_data['link']
        video_list = get_videos(link)


        #return redirect('vidlist', video_list = video_list)
        return render(request, 'channel/vidlist.html', {'video_list': video_list})
    #    return redirect('vidlist')

def video_detail(request, video_id):
    comment_output = analyze(video_id, model)

    return render(request, 'channel/video-detail.html', {'comment_output': comment_output})

def chart(request, video_id):
    comment_output = analyze(video_id, model)
    return render(request, "channel/multiple.html")
