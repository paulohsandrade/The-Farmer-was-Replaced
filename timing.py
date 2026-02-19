def time_units(time):
	hours = str(time//3600)
	if (time//60)%60 < 10:
		minutes = "0"+str((time//60)%60)
	else:
		minutes = str((time//60)%60)
	if time%60 < 10:
		seconds = "0"+str(time%60)
	else:
		seconds = str(time%60)
	return hours + ":" + minutes + ":" + seconds

def time_difference(start,end):
	time = end - start
	hours = str(time//3600)
	if (time//60)%60 < 10:
		minutes = "0"+str((time//60)%60)
	else:
		minutes = str((time//60)%60)
	if time%60 < 10:
		seconds = "0"+str(time%60)
	else:
		seconds = str(time%60)
	return hours + ":" + minutes + ":" + seconds

def sum_times(times = []):
	time = 0
	for instance in times:
		time = time + instance
	hours = str(time//3600)
	if (time//60)%60 < 10:
		minutes = "0"+str((time//60)%60)
	else:
		minutes = str((time//60)%60)
	if time%60 < 10:
		seconds = "0"+str(time%60)
	else:
		seconds = str(time%60)
	return hours + ":" + minutes + ":" + seconds