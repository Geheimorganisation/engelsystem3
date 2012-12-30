from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.conf import settings
from django.http import HttpResponse
from angelsystem.models import Blog, ShiftCategory, Shift
from collections import OrderedDict

@login_required
def index(request):
	return blog(request)

@login_required
def blog(request):
	entries = Blog.objects.all().order_by('-create_time')

	return render_to_response('blog.html', {
		'settings': settings,
		'user': request.user,
		'entries': entries
	})

@login_required
def shifts(request, date=False):
	if not date:
		the_date = _get_dates()
		if the_date:
			return redirect('angelsystem.views.shifts', date=the_date[0])

	categories = ShiftCategory.objects.all().order_by('name')
	hours = range(25)

	shift_hours = []

	for hour in hours:
		hour_shifts = []
		normalized_hour = str(hour).rjust(2, "0")

		for category in categories:
			category_shifts = category.shift_set.filter(start_time__contains='{0} {1}:'.format(date, normalized_hour))
			hour_shifts.append((category, category_shifts))
		shift_hours.append((hour, normalized_hour, hour_shifts))

	return render_to_response('all-shifts.html', {
		'settings': settings,
		'user': request.user,
		'shift_hours': sorted(shift_hours, key=lambda shift_hour: shift_hour[0]),
		'categories': categories,
		'dates': _get_dates(),
		'path': request.path
	})

@login_required
def my_shifts(request):
	return None

## helpers
def _get_dates():
	shifts = Shift.objects.all()
	dates = []

	if not shifts:
		return False

	for shift in shifts:
		start_date = shift.start_time.strftime('%Y-%m-%d')
		end_date = shift.end_time.strftime('%Y-%m-%d')
		if start_date not in dates:
			dates.append(start_date)
		if end_date not in dates:
			dates.append(end_date)

	return dates
