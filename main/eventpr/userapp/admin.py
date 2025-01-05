from django.core.mail import send_mail
from django.conf import settings
from django.contrib import admin
from .models import ChangeRequest

class ChangeRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'booking', 'request_type', 'new_value', 'status', 'created_at')
    list_filter = ('status', 'request_type')
    search_fields = ('user__username', 'booking__event_name', 'new_value')
    actions = ['approve_request', 'reject_request']

    def approve_request(self, request, queryset):
        queryset.update(status='Approved')
        for change_request in queryset:
            # Send HTML email to user about approval
            send_mail(
                'Your Change Request has been Approved',
                '',
                settings.DEFAULT_FROM_EMAIL,
                [change_request.user.email],
                fail_silently=False,
                html_message=f'''
                    <html>
                        <body>
                            <h3 style="color: green;">Change Request Approved</h3>
                            <p>Hello <strong>{change_request.user.username}</strong>,</p>
                            <p>We are pleased to inform you that your change request for the event <strong>{change_request.booking.event_name}</strong> has been approved.</p>
                            <p>The details of your updated booking are as follows:</p>
                            <ul>
                                <li><strong>Event Name:</strong> {change_request.booking.event_name}</li>
                                <li><strong>New Event Date:</strong> {change_request.booking.event_date}</li>
                                <li><strong>New Venue:</strong> {change_request.new_value}</li>
                            </ul>
                            <p>You can now proceed with the updated booking details.</p>
                            <p>If you need any further assistance, feel free to contact us.</p>
                            <p>Best regards,<br>The EventPro Team</p>
                        </body>
                    </html>
                '''
            )

    approve_request.short_description = "Approve selected change requests"

    def reject_request(self, request, queryset):
        queryset.update(status='Rejected')
        for change_request in queryset:
            # Send HTML email to user about rejection
            send_mail(
                'Your Change Request has been Rejected',
                '',
                settings.DEFAULT_FROM_EMAIL,
                [change_request.user.email],
                fail_silently=False,
                html_message=f'''
                    <html>
                        <body>
                            <h3 style="color: red;">Change Request Rejected</h3>
                            <p>Hello <strong>{change_request.user.username}</strong>,</p>
                            <p>We regret to inform you that your change request for the event <strong>{change_request.booking.event_name}</strong> has been rejected.</p>
                            <p>If you would like to discuss the reasons for the rejection or make another request, feel free to reach out to us.</p>
                            <p>Best regards,<br>The EventPro Team</p>
                        </body>
                    </html>
                '''
            )

    reject_request.short_description = "Reject selected change requests"

# Register the ChangeRequest model with the admin
admin.site.register(ChangeRequest, ChangeRequestAdmin)
