import csv
from django.http.response import HttpResponse
from django.utils.timezone import datetime


def export_to_csv(model, queryset, additional_fields=[], fields_methods={}):
    if additional_fields is None:
        additional_fields = []
    meta = model._meta
    field_names = [field.verbose_name if hasattr(field, 'verbose_name') else field.name for field in meta.fields] + additional_fields
    fields = list(meta.fields) + additional_fields
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': f'attachment; filename={model.__name__}_{datetime.today().date()}.csv'}
    )
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        row = []
        for field in fields:
            if type(field) == str:
                method = fields_methods.get(field)
                if method is not None:
                    row.append(method(obj))
                else:
                    row.append('')
            else:
                if field.is_relation:
                    value = getattr(obj, field.name)
                    row.append(f'{value};{value.id}')
                else:
                    row.append(getattr(obj, field.name))
        writer.writerow(row)
    return response


def get_verbose_name_field_dict(model):
    data = {}
    for field in model._meta.fields:
        if hasattr(field, 'verbose_name'):
            data[field.verbose_name] = field
        else:
            data[field.name] = field
    return data
