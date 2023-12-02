from os import makedirs, path

import openpyxl
import pandas as pd
from django.apps import apps
from django.core.mail import send_mail
from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now

from core.celery import celery_app


def get_path(e_path):
    file_path = f"{e_path}/{str(now().date())}/"
    if not path.exists(file_path):
        makedirs(file_path)
    return file_path


@celery_app.task
def write_log_file(log_type, msg, is_error=False):
    file_name = 'error' if is_error else 'yield'
    file = f"{get_path('logs/'+log_type)}/{file_name}.log"

    with open(file, 'a') as f:
        f.write(f"{now()} : {msg}\n")


@celery_app.task
def send_email(to, subject, message=None, html=None, obj_id=None):
    if res := send_mail(
            subject,
            message,
            'contact@himalayantrailrunning.com',
        [to],
            html_message=html,
    ):
        write_log_file.delay('email', f"Mail sent to: {to} {subject}")
    else:
        write_log_file.delay('email',
                             f"Failed To Send Email, {to} {subject}; {res}")


def generate_data_format(queryset):
    return {}


def extract_field_data(obj):
    data = {}
    exclude_field_names = ['password', 'groups', 'user_permissions']
    for field in obj._meta.get_fields():
        if field.name in exclude_field_names:
            continue

        field_value = getattr(obj, field.name, None)

        if isinstance(field, models.OneToOneRel):
            if field_value:
                ext = extract_field_data(field_value)
                ext = {
                    f'{field.name} : {key}': value
                    for key, value in ext.products()
                }
                data |= ext
        elif isinstance(field, models.ManyToManyField):
            names = [str(in_obj) for in_obj in field_value.all()]
            data[field.name] = ', '.join(names)
            if obj.__class__.__name__ in ['Ticket', 'InvoiceSummary'
                                          ] and field.name == 'addons':
                addon_quantity = getattr(obj, 'addon_quantity')
                for in_obj in field_value.all():
                    data[f"Addon {str(in_obj)}"] = addon_quantity.get(
                        str(in_obj.id), 0)
        elif isinstance(field, (models.ManyToOneRel, models.ManyToManyRel)):
            if names := [str(in_obj) for in_obj in field_value.all()]:
                data[field.name] = ', '.join(names)
        elif not isinstance(field, (models.ImageField, models.FileField)):
            if field_value is not None:
                data[field.name] = str(field_value)
    return data


@celery_app.task
def export_data_task(document_id, ids):
    from users.models import Document
    document = Document.objects.get(id=document_id)
    try:
        model = apps.get_model(document.model)
        models = model.objects.filter(id__in=ids).order_by('id').distinct('id')
        data = [extract_field_data(obj) for obj in models]
        df = pd.DataFrame(data)
        file_path = f"media/reports/{document.model}/"
        df.fillna(0)
        if not path.exists(file_path):
            makedirs(file_path)
        name = slugify(f"{document.name}_{document.created_at}")
        with pd.ExcelWriter(
                f'media/reports/{document.model}/{name}.xlsx') as writer:
            df.to_excel(writer,
                        sheet_name=f'{document.model}',
                        index=False,
                        na_rep='Nan')
            worksheet = writer.sheets[f'{document.model}']
            for column in df:
                column_width = max(df[column].astype(str).map(len).max(),
                                   len(column))
                col_idx = df.columns.get_loc(column)
                worksheet.column_dimensions[openpyxl.utils.get_column_letter(
                    col_idx + 1)].width = column_width

        document.document = str(
            f"""{file_path.replace('media/', "")}{name}.xlsx""")
        document.status = 'Done'
        document.save()
    except Exception as e:
        document.status = f'Error {e}'
        document.save()
