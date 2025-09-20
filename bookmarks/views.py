from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from listings.models import Property  # Import Property from listings app
from .models import Favorite
from django.http import JsonResponse


@login_required
def favorites(request):
    user_favorites = Favorite.objects.filter(user=request.user)
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

@login_required
def toggle_bookmark(request, property_id):
    property_obj = get_object_or_404(Property, pk=property_id)

    # Find the bookmark (Favorite) for the current user and property.
    favorite, created = Favorite.objects.get_or_create(user=request.user, property=property_obj)

    if created:
        # If the bookmark was newly created
        bookmarked = True
    else:
        # If it already existed, delete it.
        favorite.delete()
        bookmarked = False

    # If the request is an AJAX request, return a JSON response
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'bookmarked': bookmarked})

    # For non-AJAX requests, redirect to the referer or a default page
    return redirect(request.META.get('HTTP_REFERER', 'listings:property_index'))
