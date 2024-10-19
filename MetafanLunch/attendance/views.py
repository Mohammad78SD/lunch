from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
import jdatetime
from django.contrib.auth.decorators import login_required
from .models import AttendaceRecord, AttendanceRequest
from datetime import timedelta

@login_required
def attendance(request):
    user = request.user
    today = jdatetime.date.today()

    # Try to get the attendance record for today
    try:
        record = AttendaceRecord.objects.get(user=user, date=today)
    except AttendaceRecord.DoesNotExist:
        record = None

    if request.method == 'POST':
        if 'checkin' in request.POST:
            checkin_time_str = request.POST.get('checkin')
            check_in = jdatetime.datetime.strptime(checkin_time_str, '%H:%M').time()

            if record:
                messages.error(request, "شما ساعت ورود خود را ثبت کرده اید.")
            else:
                # Create a new record if it doesn't exist (first check-in)
                AttendaceRecord.objects.create(user=user, check_in=check_in, date=today)
                messages.success(request, "ساعت ورود با موفقیت ثبت شد.")
                return redirect('attendance')  # Redirect to the same view after processing

        if 'checkout' in request.POST:
            checkout_time_str = request.POST.get('checkout')
            check_out = jdatetime.datetime.strptime(checkout_time_str, '%H:%M').time()

            if record and record.check_out:
                messages.error(request, "شما ساعت خروج خود را ثبت کرده اید.")
            elif record and record.check_in:
                # Set the checkout time if the check-in time is already set
                record.check_out = check_out
                record.save()
                messages.success(request, "ساعت خروج با موفقیت ثبت شد.")
                return redirect('attendance')  # Redirect to the same view after processing

    # Pass the existing check-in/check-out times and other context to the template
    context = {
        'check_in': record.check_in if record else None,
        'check_out': record.check_out if record else None,
        'day_name': today.strftime('%A'),
        'today': today
    }

    return render(request, 'attendance/attendance.html', context)

def attendance_list(request):
    # Get the attendance records for the logged-in user
    attendances = AttendaceRecord.objects.filter(user=request.user).order_by('-date')
    return render(request, 'attendance/attendance_list.html', {'attendances': attendances})


@login_required
def change_attendance(request, attendance_id=None):
    # Retrieve the attendance record if an ID is provided
    if attendance_id:
        attendance = get_object_or_404(AttendaceRecord, id=attendance_id, user=request.user)
    else:
        attendance = None  # For new attendance requests

    if request.method == 'POST':
        # Manually retrieve data from the POST request
        requested_check_in = request.POST.get('requested_check_in')
        requested_check_out = request.POST.get('requested_check_out')
        date_str = request.POST.get('date')  # Expecting a date string in the format you define
        print(date_str)
        request_reason = request.POST.get('request_reason')

        if attendance:
        # Validate the input data
            if not requested_check_in or not requested_check_out or not request_reason:
                messages.error(request, "لطفا تمام فیلدها را پر کنید.")
                return render(request, 'attendance/attendance_edit.html', {'attendance': attendance})
            requested_date = attendance.date  # Use the existing date for the attendance record
        else:
            if not requested_check_in or not requested_check_out or not date_str or not request_reason:
                messages.error(request, "لطفا تمام فیلدها را پر کنید.")
                return render(request, 'attendance/attendance_edit.html', {'attendance': attendance})

        # Convert the date string to a jdatetime object
            try:
                requested_date = jdatetime.datetime.strptime(date_str, '%Y/%m/%d').date()  # Adjust format as needed
            except ValueError:
                messages.error(request, "فرمت تاریخ نادرست است.")
                return render(request, 'attendance/attendance_edit.html')

        # Create a new AttendanceRequest
        attendance_request = AttendanceRequest(
            user=request.user,
            attendance=attendance,  # This will be None for new requests
            requested_check_in=jdatetime.datetime.strptime(requested_check_in, '%H:%M').time(),
            requested_check_out=jdatetime.datetime.strptime(requested_check_out, '%H:%M').time(),
            date=requested_date,
            request_reason=request_reason
        )
        attendance_request.save()  # Save the change request
        messages.success(request, "درخواست تغییر با موفقیت ثبت شد.")  # Success message
        return redirect('user_requests')  # Redirect to the attendance list

    return render(request, 'attendance/attendance_edit.html', {'attendance': attendance})

def user_requests(request):
    user_requests = AttendanceRequest.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'attendance/attendance_requests.html', {'user_requests': user_requests})
