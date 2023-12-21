This app includes model admin class for csv exporting and importing.

For installation just add 'csv_admin' to your INSTALLED_APPS

For usage add in admin.py file:

```python
from csv_admin.admin import CSVExportAdmin


class MyAdmin(CSVExportAdmin):
    date_field = 'created_at'
    export_select_related = ['related_field_name']
    
    def _get_sum(self):
        sum = 1 + 2
        return sum

    def get_additional_fields(self) -> list:
        return ['sum']

    def get_additional_fields_params(self) -> dict:
        return {'sum': self._get_sum}
```