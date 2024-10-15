from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
import jdatetime
from django.contrib.auth.decorators import login_required
from .models import AttendaceRecord

@login_required
def attendance(request):
    user = request.user
    today = jdatetime.date.today()
    try:
        record = AttendaceRecord.objects.get(user=user, date=today)
    except AttendaceRecord.DoesNotExist:
        record = None
        
    if request.method == 'POST':
        if 'checkin' in request.POST:
            checkin_time_str  = request.POST.get('checkin')
            check_in = jdatetime.datetime.strptime(checkin_time_str, '%H:%M').time()
            print(check_in)
            if record:

                messages.error(request, "شما ساعت ورود خود را ثبت کرده اید.")
            else:
                # Create a new record if it doesn't exist (first check-in)
                AttendaceRecord.objects.create(user=user, check_in=check_in, date=today)
                messages.success(request, "ساعت ورود با موفقیت ثبت شد.")
                
        if 'checkout' in request.POST:
            checkout_time_str = request.POST.get('checkout')
            check_out = jdatetime.datetime.strptime(checkout_time_str, '%H:%M').time()
            if record.check_out:
                messages.error(request, "شما ساعت خروج خود را ثبت کرده اید.")
            elif record and record.check_in:
                # Set the checkout time if the check-in time is already set
                record.check_out = check_out
                record.save()
                messages.success(request, "ساعت خروج با موفقیت ثبت شد.")
    
    # Pass the existing check-in/check-out times and other context to the template
    context = {
        'check_in': record.check_in if record else None,
        'check_out': record.check_out if record else None,
        'day_name': today.strftime('%A'),
        'today': today
    }
    print(context)
    
    return render(request, 'attendance/attendance.html', context)

def attendance_list(request):
    # Get the attendance records for the logged-in user
    attendances = AttendaceRecord.objects.filter(user=request.user).order_by('-date')
    return render(request, 'attendance/attendance_list.html', {'attendances': attendances})



def change_attendance(request, attendance_id=None):
    if attendance_id:
        attendance = get_object_or_404(AttendaceRecord, id=attendance_id, user=request.user)
    else:
        attendance = None  # For new attendance requests

    if request.method == 'POST':

        if attendance:
            change_request.attendance = attendance
        else:
            # Create a new attendance record for a previous day (pending admin approval)
            attendance = Attendance.objects.create(
                user=request.user,
                check_in=form.cleaned_data['requested_check_in'],
                check_out=form.cleaned_data['requested_check_out'],
                date=form.cleaned_data['date'],  # Assuming you add a date field in the form
                is_finalized=False
            )
            change_request.attendance = attendance
        change_request.save()
        return redirect('attendance_list')
    else:
        form = AttendanceChangeRequestForm()

    return render(request, 'request_change.html', {'form': form, 'attendance': attendance})