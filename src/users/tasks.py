from core.celery import celery_app
from core.settings.environments import DEBUG
from core.tasks import write_log_file
from django.apps import apps
from django.core.mail import send_mail
from django.template.loader import render_to_string


@celery_app.task
def send_otp_email(id):
    try:
        model = apps.get_model('users.VerificationCode')
        obj = model.objects.get(id=id)
        if DEBUG:
            redirect = (
                'https://apihtr.himalayancreatives.com/api/users/verify/'
                f'?{obj.hash}')
        else:
            redirect = (
                'https://api.himalayantrailrunning.com/api/users/verify/'
                f'?{obj.hash}')
        if msg_html := render_to_string('verify.html', {'redirect': redirect}):
            if _ := send_mail(
                    subject="Verify for Himalayan Trail Running Account",
                    message="",
                    from_email='contact@himalayantrailrunning.com',
                    recipient_list=[obj.email],
                    html_message=msg_html,
                    fail_silently=False):
                obj.is_email_sent = True
                obj.save()
    except Exception as exp:
        write_log_file('otp', f'error for {obj.email} : {exp}', True)
