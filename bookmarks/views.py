from django.shortcuts import render

def favorites(request):
    return render(request, 'bookmarks/favorites.html')