from django.contrib.auth import get_user_model
from django.db import models
from django_jalali.db import models as jmodels
import jdatetime
from datetime import datetime, timedelta
from django.db.models import Q
User = get_user_model()

class AttendaceRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = jmodels.jDateField(default=jdatetime.date.today())
    check_in = models.TimeField()
    check_out = models.TimeField(null=True, blank=True)
    
    @classmethod
    def total_attendance_duration_this_month(cls, user):
        if jdatetime.datetime.now().day < 21:
            year = jdatetime.datetime.now().year
            month = jdatetime.datetime.now().month
            j_start_date = jdatetime.date(year, month, 21).replace(month=month-1)
            j_end_date = jdatetime.date(year, month, 20)

        else:
            year = jdatetime.datetime.now().year
            month = jdatetime.datetime.now().month
            j_start_date = jdatetime.date(year, month, 21)
            j_end_date = jdatetime.date(year, month, 20).replace(month=month+1)
        date_range_query = Q(date__gte=j_start_date) & Q(date__lte=j_end_date)

        attendances = cls.objects.filter(user=user).filter(date_range_query)
        total_duration = timedelta()
        for attendance in attendances:
            total_duration += attendance.duration()
        
        return total_duration.total_seconds() / 3600
    
    def duration(self):
        # Combine the date with the check-in and check-out times to create datetime objects
        check_in_datetime = datetime.combine(datetime.today(), self.check_in)
        if self.check_out is None:
            self.check_out = datetime.now().time()
        check_out_datetime = datetime.combine(datetime.today(), self.check_out)
        # look here i want to minos 1 hour from duration if checkin time is between 9 and 11.30 am 
        if check_in_datetime.time() > datetime.strptime('09:00', '%H:%M').time() and check_in_datetime.time() < datetime.strptime('11:30', '%H:%M').time() and check_out_datetime.time() > datetime.strptime('12:30', '%H:%M').time(): 
            duration = check_out_datetime - check_in_datetime - timedelta(hours=1)
        else:
            duration = check_out_datetime - check_in_datetime

        return duration
    
    def __str__(self):
        return f'{self.user} روز {self.date.strftime("%A %Y/%m/%d")}'
    
    def set_default_checkou(self):
        if self.check_in and not self.check_out:
            self.check_out = self.check_in.replace(hour=16, minute=0)
            self.save()
    
    def save(self, *args, **kwargs):
        if self.check_in and self.check_out and self.check_in > self.check_out:
            raise ValueError('ساعت ورود نمی‌تواند از ساعت خروج جلوتر باشد.')
        super().save(*args, **kwargs)
        
        
class AttendanceRequest(models.Model):
    # if its a new attendance
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = jmodels.jDateField(null=True, blank=True)
    
    attendance = models.ForeignKey(AttendaceRecord, on_delete=models.CASCADE, related_name='change_requests', null=True, blank=True)
    requested_check_in = models.TimeField(null=True, blank=True)
    requested_check_out = models.TimeField(null=True, blank=True)
    request_reason = models.TextField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
    created_at = jmodels.jDateTimeField(auto_now_add=True)

    def __str__(self):
        return f"درخواست بازبینی {self.user.last_name} - {self.created_at}"
    
    def save(self, *args, **kwargs):
        if self.status == 'approved':
            if self.attendance:
                self.attendance.check_in = self.requested_check_in
                self.attendance.check_out = self.requested_check_out
                self.attendance.save()
            else:
                self.attendance = AttendaceRecord.objects.create(user=self.user, date=self.date, check_in=self.requested_check_in, check_out=self.requested_check_out)
        super().save(*args, **kwargs)
        
    