import csv
from decimal import Decimal
from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.utils import timezone
from csv_admin.utils import export_to_csv, get_verbose_name_field_dict


class CSVExportAdmin(admin.ModelAdmin):
    """ModelAdmin class which allows you to import/export model data to csv.

    Also, you have options to delete all data of the model.

    If you want to include any custom fields, then you should implement get_additional_fields method, which include
    names of this custom fields, default returns an empty list.
    Example:
        def get_additional_fields(self) -> list:
            return ['custom_field_name']
    Also, you should implement get_additional_field_params method, which returns dict where key is the name of custom
    field and value is the method which returns value or data of this field.
    Example:
        def get_additional_field_params(self) -> dict:
            return {'custom_field_name': self._get_custom_field}

    ::params
    export_select_related - array with select related fields
    date_field - enables date filtering, if you want to specify from which date you want export your data
    start_date_expression - default 'gte'
    end_date_expression - default, 'lte'
    """
    change_list_template = 'csv_admin/add_csv_export_changelist.html'
    export_select_related = None
    date_field = None
    start_date_expression = 'gte'
    end_date_expression = 'lte'

    def get_urls(self):
        return [
            path('make-table/', self.admin_site.admin_view(self.export), name=f'{self.model.__name__.lower()}_make_table'),
            path('delete-all/', self.admin_site.admin_view(self.delete_all_data), name=f'{self.model.__name__.lower()}_delete_all'),
            path('import/', self.admin_site.admin_view(self.import_data_from_csv), name=f'{self.model.__name__.lower()}_import_data')
        ] + super().get_urls()

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['make_table_url'] = f'admin:{self.model.__name__.lower()}_make_table'
        extra_context['delete_all_url'] = f'admin:{self.model.__name__.lower()}_delete_all'
        extra_context['import_data_url'] = f'admin:{self.model.__name__.lower()}_import_data'
        return super().changelist_view(request, extra_context)

    def get_additional_fields(self) -> list:
        return []

    def get_additional_fields_params(self) -> dict:
        return {}

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        if self.date_field is not None:
            if isinstance(list_display, tuple) and self.date_field not in list_display:
                return list_display + (self.date_field,)
            if isinstance(list_display, list) and self.date_field not in list_display:
                return list_display + [self.date_field]
        return list_display

    @csrf_exempt
    def export(self, request):
        try:
            start_time = timezone.datetime.fromisoformat(request.POST['start_time'])
        except Exception:
            start_time = None

        try:
            end_time = timezone.datetime.fromisoformat(request.POST['end_time'])
        except Exception:
            end_time = None

        qs = self.model.objects.all()

        filter_kwargs = None
        if start_time and self.date_field:
            filter_kwargs = {f'{self.date_field}__{self.start_date_expression}': start_time}
        if end_time and self.date_field:
            filter_kwargs = {f'{self.date_field}__{self.start_date_expression}': start_time}

        if filter_kwargs is not None:
            qs = qs.filter(**filter_kwargs)

        if self.export_select_related is not None:
            qs = qs.select_related(*self.export_select_related)
        return export_to_csv(self.model, qs, self.get_additional_fields(), self.get_additional_fields_params())

    @csrf_exempt
    def delete_all_data(self, request):
        self.model.objects.all().delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    @csrf_exempt
    def import_data_from_csv(self, request):
        file = request.FILES['file']
        decoded_file = file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        fields = get_verbose_name_field_dict(self.model)
        for row in reader:
            model_data = {}
            for key, value in row.items():
                field = fields.get(key)
                if field:
                    if field.is_relation:
                        value = value.split(';')[1]
                        model_data[f'{field.name}_id'] = int(value)
                    else:
                        model_data[field.name] = Decimal(value) if hasattr(field, 'decimal_places') else value
            self.model.objects.create(**model_data)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
