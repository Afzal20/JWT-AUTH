from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Profil
from django.utils.html import format_html

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email',)  # Use 'email' as the login field instead of 'username'


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'password')  # Customize based on your model fields


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm  # Form used when creating a user
    form = CustomUserChangeForm  # Form used when changing user details
    model = CustomUser  # The custom user model

    list_display = ('email', 'name', 'is_staff', 'is_active')  # Fields shown in the admin list view
    list_filter = ('is_staff', 'is_active')  # Filters in the admin list view
    fieldsets = (
        (None, {'fields': ('email', 'name', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )  # What is displayed when viewing a single user in the admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )  # What is displayed when adding a new user in the admin
    search_fields = ('email',)
    ordering = ('email',)


class ProfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'image_tag', 'description', 'address', 'phone', 'NumberOfOrders', 'orders')
    
    # Function to display the image as a thumbnail in the admin panel
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.image.url))
        else:
            return 'No Image'

    image_tag.short_description = 'Profile Image'



admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profil, ProfilAdmin)
