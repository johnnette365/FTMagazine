from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone

# Create your models here.



# SEO Meta Fields Mixin
class SEOMixin(models.Model):
    meta_title = models.CharField(max_length=60, blank=True, null=True, help_text="Title for SEO (Max: 60 characters)")
    meta_description = models.CharField(max_length=160, blank=True, null=True, help_text="Description for SEO (Max: 160 characters)")
    meta_keywords = models.CharField(max_length=255, blank=True, null=True, help_text="Comma-separated keywords (Max: 10 keywords)")

    class Meta:
        abstract = True



# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name



# Tag Model
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name



class Magazine(SEOMixin):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True) 
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    cover_image = models.ImageField(upload_to='Magazines/Cover_images/', blank=True, null=True)  
    cover_video = models.FileField(upload_to='Magazines/Cover_videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # FIXED
    published_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title



# Magazine Sections (Supports Images, Videos, and Text)
class MagazineSection(models.Model):
    magazine = models.ForeignKey(Magazine, on_delete=models.CASCADE, related_name="sections")
    heading = models.CharField(max_length=255, blank=True, null=True)
    content_top = RichTextField(blank=True, null=True)  # Content before media
    image = models.ImageField(upload_to='Magazines/sections/', blank=True, null=True)  # Optional Image
    image_caption = models.CharField(max_length=255, blank=True, null=True)  # Caption for media
    video = models.FileField(upload_to='Magazines/videos/', blank=True, null=True)  # Optional Video Upload
    external_video_url = models.URLField(blank=True, null=True)  # External video (YouTube, Vimeo, etc.)
    content_bottom = RichTextField(blank=True, null=True)  # Content after media

    def __str__(self):
        return f"Section: {self.heading if self.heading else 'No Heading'}"



# Comment Model (For Magazines & News)
class Comment(models.Model):
    magazine = models.ForeignKey(Magazine, on_delete=models.CASCADE, related_name="comments", blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user}"
    


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email