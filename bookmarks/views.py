from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from listings.models import Property # Property 모델은 listings 앱에서 가져옵니다.
from .models import Favorite # Favorite 모델은 현재 앱에서 가져옵니다.
from django.http import HttpResponse, JsonResponse # JsonResponse 추가


@login_required
def favorites(request):
    user_favorites = Favorite.objects.filter(user=request.user).select_related('property')

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
    if request.method == 'POST':
        property_obj = get_object_or_404(Property, pk=property_id)
        
        # 현재 유저와 해당 매물에 대한 북마크(Favorite)를 찾습니다.
        favorite, created = Favorite.objects.get_or_create(user=request.user, property=property_obj)

        if created:
            # 북마크가 새로 생성되었으면
            bookmarked = True
        else:
            # 이미 존재하면 삭제합니다.
            favorite.delete()
            bookmarked = False

        return JsonResponse({'bookmarked': bookmarked})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)