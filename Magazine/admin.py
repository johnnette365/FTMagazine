from django.contrib import admin
from .models import Category, Tag, Magazine, MagazineSection, Comment, Subscriber

# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)} 



# Tag Admin
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# Inline Model for Magazine Sections
class MagazineSectionInline(admin.StackedInline):  # or admin.StackedInline
    model = MagazineSection
    extra = 1


# Magazine Admin
@admin.register(Magazine)
class MagazineAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'is_published', 'published_at')
    list_filter = ('is_published', 'category', 'tags', 'created_at', 'published_at')
    search_fields = ('title', 'meta_title', 'meta_description', 'meta_keywords')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    filter_horizontal = ('tags',)
    inlines = [MagazineSectionInline]


# Comment Admin
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'magazine', 'created_at')
    list_filter = ('created_at', 'magazine')
    search_fields = ('user__username', 'content')




@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')  # Display these fields in admin panel
    search_fields = ('email',)  # Allow search by email
    ordering = ('-subscribed_at',)  # Show the latest subscriptions first