from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Favorite, Property
from django.contrib.auth.models import User
from django.http import HttpResponse
from bookmarks.models import Favorite


@login_required
def favorites(request):
    user = request.user
    username = user.username
    favorites = Favorite.objects.all()
    user_favorites = Favorite.objects.filter(user_id=user)  # user_id에 맞게 변경

    # 1. 로그인 유저의 즐겨찾기
    user_favorites = Favorite.objects.filter(user=user).select_related('property')

    # 2. 즐겨찾기한 Property 객체만 가져오기
    properties = [fav.property for fav in user_favorites]
    context = {
        "favorites": properties,
        "user_id": user
    }

    return render(request, "bookmarks/favorites.html", context)


@require_POST
@login_required
def remove_favorite(request, property_id):
    # 로그인한 유저의 해당 즐겨찾기만 조회
    favorite = get_object_or_404(Favorite, user=request.user, property_id=property_id)
    # 삭제
    favorite.delete()
    # 즐겨찾기 페이지로 리다이렉트
    return redirect('bookmarks:favorites')