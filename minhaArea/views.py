from django.shortcuts import render

def area(request):
    return render(request, 'minhaArea/area.html')
