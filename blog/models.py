from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver

# --- Category ---
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# --- Tag ---
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# --- Post ---
class Post(models.Model):
    author = models.ForeignKey('core.User', on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField('core.User', related_name='liked_posts', blank=True)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()


def generate_unique_slug(instance, field_name='title', max_length=50):
    slug_base = slugify(getattr(instance, field_name))[:max_length]
    slug = slug_base
    ModelClass = instance.__class__
    num = 1

    while ModelClass.objects.filter(slug=slug).exclude(pk=instance.pk).exists():
        slug = f"{slug_base}-{num}"
        num += 1

    return slug


@receiver(pre_save, sender=Post)
def post_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = generate_unique_slug(instance, 'title', max_length=50)
