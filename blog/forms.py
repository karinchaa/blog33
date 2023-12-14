from django import forms
from django.db import IntegrityError
from .models import Post, Comment, UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    date_of_birth = forms.DateField(required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'date_of_birth', 'profile_picture')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            try:
                user.save()
            except IntegrityError:
                raise forms.ValidationError('User with this username already exists.')
            try:
                UserProfile.objects.create(user=user, date_of_birth=self.cleaned_data['date_of_birth'])
            except IntegrityError:
                user.delete()
                raise forms.ValidationError('User profile for this username already exists.')

        return user


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'tag', 'poster']
        widgets = {
            'tag': forms.CheckboxSelectMultiple,
        }


class ImageForm(forms.Form):
    image = forms.ImageField(label='Image', required=False)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('post', 'published_date', 'author')


class SubscriptionForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=254)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['date_of_birth', 'profile_picture']