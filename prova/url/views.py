from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
import random
import string

from .serializers import UrlSerializer
from .forms import URLForm
from .models import Url


# Create your views here.


def index(request):
    form_vazio = URLForm()
    encurtado = random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(
        string.ascii_letters) + random.choice(string.ascii_letters)
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            url_grande = request.POST['url_grande']
            obj = form.save()
            obj.hash = encurtado
            obj.save()
            return render(request, 'index.html', {'url': obj, 'form': form_vazio})
    else:
        form = URLForm()
        return render(request, 'index.html', {'form': form})


def redirect_url(request, slug):
    url = Url.objects.get(hash=slug)
    return redirect(url.url_grande)


@api_view(['GET', 'POST'])
def url_list(request):
    if request.method == 'GET':
        url = Url.objects.get()
        serializer = UrlSerializer(url, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UrlSerializer(data=request.data)
        encurtado = random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(
            string.ascii_letters) + random.choice(string.ascii_letters)
        if serializer.is_valid():
            try:
                serializer.validated_data['hash'] = encurtado
                serializer.save()
                return Response('http://localhost:8000/api/' + serializer.data['hash'], status=200)
            except:
                return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def url_detail(request, slug):
    try:
        url = Url.objects.get(hash=slug)
    except Url.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = UrlSerializer(url)
        return Response(serializer.data)
