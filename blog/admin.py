from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, BlogPost, Comment
from .forms import CustomUserChangeForm, CustomUserCreationForm

# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_filter = ("email",)
    list_display = ("email",)
    
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password", "is_staff", "is_active", "is_superuser", "groups", "user_permissions",
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


class BlogPostAdmin(admin.ModelAdmin):
    model = BlogPost
    list_display = ["author", "title", "body"]


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ["sender", "message", "timestamp"]

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Comment, CommentAdmin)