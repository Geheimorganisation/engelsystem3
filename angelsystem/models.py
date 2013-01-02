from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

## SHIFTS

class ShiftCategory(models.Model):
	name = models.CharField(unique=True, max_length=30)
	arch = models.ForeignKey(User, limit_choices_to={'is_staff': True})

	def __unicode__(self):
		return self.name

class ShiftLocation(models.Model):
	location = models.CharField(unique=True, max_length=30)

	def __unicode__(self):
		return self.location

class ShiftLocationAdmin(admin.ModelAdmin):
	list_display = ['location']

class Shift(models.Model):
	category = models.ForeignKey('ShiftCategory')
	location = models.ForeignKey('ShiftLocation')
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	max_angels = models.PositiveIntegerField()
	users = models.ManyToManyField(User, blank=True)

	def required_angels(self):
		return self.max_angels - self.users.count()

class ShiftAdmin(admin.ModelAdmin):
	list_display = ['category', 'location', 'start_time', 'end_time', 'max_angels']
	list_filter = list_display

## BLOG

class Blog(models.Model):
	arch = models.ForeignKey(User, limit_choices_to={'is_staff': True})
	title = models.CharField(max_length=30)
	content = models.TextField()
	create_time = models.DateTimeField(auto_now_add=True)
	pin = models.BooleanField()

class BlogAdmin(admin.ModelAdmin):
	list_display = ['title', 'create_time']

admin.site.register(ShiftCategory)
admin.site.register(ShiftLocation, ShiftLocationAdmin)
admin.site.register(Shift, ShiftAdmin)
admin.site.register(Blog, BlogAdmin)
