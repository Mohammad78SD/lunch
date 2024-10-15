from django.db import models
from django_jalali.db import models as jmodels
from lunch.models import CustomUser as User
import jdatetime
from datetime import datetime

class AttendaceRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = jmodels.jDateField(default=jdatetime.date.today())
    check_in = models.TimeField()
    check_out = models.TimeField(null=True, blank=True)
    
    def duration(self):
        # Combine the date with the check-in and check-out times to create datetime objects
        check_in_datetime = datetime.combine(datetime.today(), self.check_in)
        check_out_datetime = datetime.combine(datetime.today(), self.check_out)

        # Calculate the difference between check-out and check-in
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
    
    attendance = models.ForeignKey(AttendaceRecord, on_delete=models.CASCADE, related_name='change_requests')
    requested_check_in = models.TimeField(null=True, blank=True)
    requested_check_out = models.TimeField(null=True, blank=True)
    request_reason = models.TextField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"درخواست بازبینی {self.user.last_name} - {self.attendance.date}"
    
    def save(self, *args, **kwargs):
        if self.status == 'approved':
            if self.attendance:
                self.attendance.check_in = self.requested_check_in
                self.attendance.check_out = self.requested_check_out
                self.attendance.save()
            else:
                self.attendance = AttendaceRecord.objects.create(user=self.user, date=self.date, check_in=self.requested_check_in, check_out=self.requested_check_out)
        super().save(*args, **kwargs)