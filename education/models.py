from django.db import models

class Article(models.Model):
    """Educational articles"""
    
    CATEGORIES = [
        ('nutrition', 'Nutrition'),
        ('transition', 'Food Transition'),
        ('health', 'Health & Wellness'),
        ('training', 'Training & Behavior'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    content = models.TextField()
    summary = models.TextField(max_length=300)
    
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title