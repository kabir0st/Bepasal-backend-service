import os
from PIL import Image
import random
import string
from functools import wraps
from rest_framework.exceptions import APIException
import dateutil.parser
from core.tasks import export_data_task
from django.core.cache import cache
from django.db.transaction import atomic
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


def are_model_fields_equal(obj1, obj2, *fields):
    values_to_compare_obj1 = [getattr(obj1, field) for field in fields]
    values_to_compare_obj2 = [getattr(obj2, field) for field in fields]
    return values_to_compare_obj1 == values_to_compare_obj2


class InfinitePagination(PageNumberPagination):
    page_size = 10  # Set the number of items to be returned per page
    page_size_query_param = 'page_size'
    max_page_size = 1000  # Optionally set a maximum page size


def copy_model(from_model, to_model, reference_class=None):
    obj = to_model()
    reference = reference_class or from_model
    exclude = ['created_at', 'updated_at', 'uuid', 'slug']
    for field in reference._meta.get_fields():
        if field.name in exclude:
            continue
        try:
            setattr(obj, field.name, getattr(from_model, field.name))
        except Exception as exp:
            raise APIException(exp) from exp
    return obj


def grab_error(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            with atomic():
                return func(*args, **kwargs)
        except Exception as exp:
            return Response(
                {
                    'status': False,
                    'error': f'{exp.__class__.__name__}: {exp}'
                },
                status=status.HTTP_400_BAD_REQUEST)

    return wrapper


def is_token_valid(token):
    return cache.get(token)


def split_word_for_search(word):
    words = word.split(' ')
    for x in words:
        if x == '':
            words.pop(x)
    return words


def remove_spaces(word):
    result = ''
    word = list(word)
    last_word_space = True
    for w in word:
        if w == ' ':
            if not last_word_space:
                last_word_space = True
                result = result + w
        else:
            last_word_space = False
            result = result + w
    return result


def default_array():
    return []


def default_json():
    return {}


def str_to_datetime(datetime_str):
    return dateutil.parser.parse(datetime_str)


def parse_range(ranges):
    try:
        ranges = str(ranges).replace('[', '').replace(']', '').replace(
            '(', '').replace(')', '')
        ranges = ranges.split(',')
        return {'from': ranges[0], 'upto': ranges[1]}
    except Exception as exp:
        raise APIException(
            f'Ranges must be given in [__from__, __upto__]'
            f' or (__from__, __upto__) format. Error: {exp}') from exp


def validate_order_by(valid_orders, order_by):
    des = ''
    if order_by[:1] == "-":
        des = order_by[:1]
        order_by = order_by[1:]
    if order_by.lower() in valid_orders:
        return f"{des}{order_by.lower()}"
    else:
        raise APIException(f"{order_by} is a Invalid order argument.")


def clean_data(keys, data):
    for key in keys:
        data.pop(key, None)
    return data


def generate_upload_location(instance, filename):
    if hasattr(instance, 'slug'):
        return f'{instance.__class__.__name__}/{instance.slug}/{filename}'
    return f'{instance.__class__.__name__}/{instance.id}/{filename}'


def export_data(model, ids, document_name=None):
    from users.models.supports import Document
    document = Document.objects.create(model=model, name=document_name)
    export_data_task(document.id, ids)
    return document.id


def optimize_image(image, output_image_path):
    max_size_kb = 120
    desired_ppi = 72
    max_width = 600
    if max(image.size) > max_width:
        ratio = max_width / image.size[1]
        new_size = tuple(int(x * ratio) for x in image.size)
        image = image.resize(new_size, Image.Resampling.LANCZOS)
    width, height = image.size
    width_inch = width / desired_ppi
    height_inch = height / desired_ppi
    image = image.resize((int(width_inch * 72), int(height_inch * 72)),
                         Image.Resampling.LANCZOS)
    characters = string.ascii_letters
    temp_path = ''.join(random.choice(characters) for _ in range(10))
    quality = 100
    image.save(temp_path, 'webp', quality=quality)
    temp_size = os.path.getsize(temp_path)
    while temp_size > (max_size_kb * 1024) and quality > 60:
        quality -= 5
        image.save(temp_path, 'webp', quality=quality)
        temp_size = os.path.getsize(temp_path)
    os.rename(temp_path, output_image_path)
    return output_image_path
