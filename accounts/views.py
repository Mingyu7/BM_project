from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import UserProfile
from listings.models import Property
from bookmarks.models import Favorite
from .forms import UserProfileForm

@login_required
def profile_update(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        # If profile does not exist, create one
        profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:my_page')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'accounts/profile_update.html', {'form': form})

@login_required
def my_page(request):
    user = request.user
    try:
        user_profile = user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = None

    # Fetch properties created by the user
    user_posts = Property.objects.filter(author=user)

    # Fetch user's bookmarked/favorited properties
    applications = Favorite.objects.filter(user=user)

    context = {
        'user_info': user_profile, # Passing the profile
        'user': user, # Passing the default user object as well
        'user_posts': user_posts,
        'applications': applications,
    }
    return render(request, 'accounts/my_page.html', context)

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='아이디', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'accounts/login.html'

class SignUpForm(UserCreationForm):
    name = forms.CharField(max_length=100, label='이름', widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(max_length=20, label='전화번호', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    terms_agreement = forms.BooleanField(
        label='이용약관 및 개인정보 처리방침에 동의합니다.',
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = '아이디'
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("중복된 아이디 입니다.")
        return username

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create the UserProfile with the name and phone_number from the form
            UserProfile.objects.create(user=user, name=form.cleaned_data['name'], phone_number=form.cleaned_data.get('phone_number'))
            return redirect('accounts:login')
        else:
            # Print form errors to the console for debugging
            print("Form is not valid. Errors:", form.errors)
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})
