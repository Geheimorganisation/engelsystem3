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
		return redirect('angelsystem.views.shifts', date=_getDates()[0])

	categories = ShiftCategory.objects.all().order_by('name')
	sorted_out = {}
	day_range = range(25)
	out = OrderedDict()

	for h in day_range:
		normalized = str(h).rjust(2, "0")
		out[normalized] = OrderedDict()

		for cat in categories:
			out[normalized][cat.name] = []

			for shift in cat.shift_set.filter(start_time__contains='{0} {1}:'.format(date, normalized)):
				shift.start_time = shift.start_time.strftime("%H:%M")
				shift.end_time = shift.end_time.strftime("%H:%M")
				out[normalized][cat.name].append(shift)

	return render_to_response('all-shifts.html', {
		'settings': settings,
		'user': request.user,
		'shifts': sorted(out.items()),
		'categories': categories,
		'dates': _getDates(),
		'path': request.path
	})

@login_required
def myShifts(request):
	return None

## helpers
def _getDates():
	shifts = Shift.objects.all()
	dates = []

	for shift in shifts:
		start_date = shift.start_time.strftime('%Y-%m-%d')
		end_date = shift.end_time.strftime('%Y-%m-%d')
		if start_date not in dates:
			dates.append(start_date)
		if end_date not in dates:
			dates.append(end_date)

	return dates