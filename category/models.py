from django.db import models
from markdown.extensions.toc import slugify
from rest_framework.reverse import reverse


class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=False)
    description = models.TextField(max_length=255, blank=True, null=True)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True, null=True)

    def generate_slug(self):
        slug = slugify(self.category_name, '-')
        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()
        return super().save(*args, **kwargs)

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    class Meta:
        verbose_name_plural = 'Categories'
        verbose_name = 'Category'

    def __str__(self):
        return self.category_name
