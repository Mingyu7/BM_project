from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Favorite, Property
from django.contrib.auth.models import User
from django.http import HttpResponse
from bookmarks.models import Favorite


@login_required
def favorites(request):
    favorites = Favorite.objects.all()
    user_favorites = Favorite.objects.filter(user_id=3)  # user_id에 맞게 변경

    context = {
        "favorites": user_favorites,
    }
    return render(request, "bookmarks/favorites.html", context)

@require_POST
@login_required
def remove_favorite(request, property_id):
    property_to_remove = get_object_or_404(Property, pk=property_id)
    favorite = get_object_or_404(Favorite, user=request.user, property=property_to_remove)
    favorite.delete()
    return redirect('bookmarks:favorites')