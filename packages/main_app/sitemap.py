from django.core.urlresolvers import reverse
from django.contrib.sitemaps import Sitemap
from .models import Post, Category


class MainSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9
    
    def items(self):
        return Post.objects.filter(status='p')
    
    def lastmod(self, obj):
        return obj.publish_date


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    
    def items(self):
        return Category.objects.all()


class OtherSitemap(Sitemap):
    def items(self):
        return [
            {
                'name': 'main_app:index',
                'change': 'daily',
                'pri': '1.0'
            },
            {
                'name': 'signup',
                'change': 'never',
                'pri': '0.7'
            },
            {
                'name': 'login',
                'change': 'never',
                'pri': '0.6'
            },
            {
                'name': 'terms',
                'change': 'yearly',
                'pri': '0.5'
            },
        ]
    
    def location(self, item):
        return reverse(item['name'])
    
    def changefreq(self, item):
        return item['change']
    
    def priority(self, item):
        return item['pri']
