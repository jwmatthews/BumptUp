from tastypie.utils.timezone import now
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Category(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=5000)
    created = models.DateTimeField(default=now)
    modified = models.DateTimeField()
    display = models.BooleanField()
    slug = models.SlugField()
    owner = models.ForeignKey(User)

    def __unicode__(self):
        return "%s:  %s" % (self.owner, self.description)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:50]
        return super(Category, self).save(*args, **kwargs)

class Rating(models.Model):
    score = models.IntegerField()
    category = models.ForeignKey(Category)
    rater = models.ForeignKey(User)
    created = models.DateTimeField(default=now)

    def __unicode__(self):
        return "%s: %s: %s" % (self.rater, self.score, self.category)
