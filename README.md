# Django jQuery DataTables

Django jQuery DataTables is a Python library that integrates the popular jQuery DataTables library with Django projects. It provides a convenient way to handle and manage datatables in your Django application.

## Features

- Integration with jQuery DataTables for efficient data table handling.
- Support for main search and individual column search.
- Flexible column remapping for customized data filtering.
- Pagination support for large datasets.
- Easy serialization of data using Django serializers.

## Installation

You can install Django jQuery DataTables using `pip install django_jquery_datatables`:

## Usage

To use Django jQuery DataTables in your Django project, follow these steps:

1. Install Django jQuery DataTables by `pip install django_jquery_datatables`.
2. Import the main datatables function by using `from django_jquery_datatables.utils import JqueryDatatable`
3. This JqueryDatatable is used in the view function of django, it returns all the data required by jquery datatables library in the form of JSON.

## Basic Example

#####Frontend:

```html
<table id="users_table" class="table">
    <thead>
    <tr>
        <th>Username</th>
        <th>Is Staff</th>
        <th>Is Superuser</th>
        <th>Is Active</th>
        <th>Last Login</th>
    </tr>
    </thead>
</table>
<script>
    $(document).ready(function () {
        $('#users_table').DataTable({
            dom: 'Bfrtip',
            order: [],
            orderCellsTop: true,
            "processing": true,
            "serverSide": true,
            ajax: {
                url: '/django_jquery_datatable_url/',
                type: 'GET',
                contentType: 'application/json',
            },
            columns: [
                {data: "username"},
                {data: "is_staff"},
                {data: "is_superuser"},
                {data: "is_active"},
                {data: "last_login"},
            ],
            "createdRow": function (row, data, dataIndex) {
                $(row).attr("id", data.id);
            },
            buttons: [
                'copy', 'csv', 'excel', 'pdf', 'print', 'pageLength'
            ],
            lengthMenu: [
                [10, 50, 100, 500],
                ["10 rows", "50 rows", "100 rows", "500 rows"],
            ],
            pageLength: 10,
        });
    });
</script>
```
##### Django Backend
```python
from django.contrib.auth.models import User
from django_jquery_datatables.utils import JqueryDatatable
from rest_framework import serializers


class UsersSerializer(serializers.ModelSerializer):
    DT_RowId = serializers.IntegerField(source='id')

    class Meta:
        model = User
        exclude = ['password']


def my_view(request):
    queryset = User.objects.all()
    # You can also sort the initial data here.
    return JqueryDatatable(request, queryset, UsersSerializer)

```

## Advance Examples
### 1. Individual Column Search
For adding search to each individual column in datatables, there is no need to change backend logic, you only need to 
add search to your jquery code, here is an example usage with seach at the top of every column.
```html
<table id="users_table" class="table">
    <thead>
    <tr>
        <th>Username</th>
        <th>Is Staff</th>
        <th>Is Superuser</th>
        <th>Is Active</th>
        <th>Last Login</th>
    </tr>
    </thead>
</table>
<script>
    $(document).ready(function () {
        $('#users_table thead tr').clone(true).appendTo('#users_table thead');
        $('#users_table thead tr:eq(1) th').each(function (i) {
            var title = $(this).text();
            // Here you can specify the column names on which you do not want to add a search
            if (['Remove', 'Edit', 'Action'].includes(title)) {
                $(this).html('');
            } else {
                $(this).html(`<div class="col-xs-2"><input style="height:10px;" name="${title}" placeholder="Search" class="form-control" type="text"></div>`);
                $('input', this).on('keyup change', function () {
                    if (table.column(i).search() !== this.value) {
                        table.column(i).search(this.value).draw();
                    }
                });
            }
        });
        var table = $('#users_table').DataTable({
            dom: 'Bfrtip',
            order: [],
            orderCellsTop: true,
            "processing": true,
            "serverSide": true,
            ajax: {
                url: '/django_jquery_datatable_url/',
                type: 'GET',
                contentType: 'application/json',
            },
            columns: [
                {data: "username"},
                {data: "is_staff"},
                {data: "is_superuser"},
                {data: "is_active"},
                {data: "last_login"},
            ],
            "createdRow": function (row, data, dataIndex) {
                $(row).attr("id", data.id);
            },
            buttons: [
                'copy', 'csv', 'excel', 'pdf', 'print', 'pageLength'
            ],
            lengthMenu: [
                [10, 50, 100, 500],
                ["10 rows", "50 rows", "100 rows", "500 rows"],
            ],
            pageLength: 10,
        });
    });
</script>
```
Backend code remains the same as provided previously

### 2. Custom Columns Maping
This feature is very handful when you're having a custom field defined in your 
serializer which is not present in your database, by doing this search will be done using 'bar' which is present in your model.<br>
To do this you can simple pass and array of python dict with the name of field and the model field in values.
```python
return JqueryDatatable(request, queryset, UsersSerializer, [ {'foo': 'bar'} ])
```
#### a) Maping single column
In this example you can map one column which is defined in your serializer to any column present in your model
For Example: <br>
A field named 'foo' is defined in serializer which you want to map with a field 'bar' in your model you can map it as: <br>
```python
from django.contrib.auth.models import User
from django_jquery_datatables.utils import JqueryDatatable
from rest_framework import serializers

class UsersSerializer(serializers.ModelSerializer):
    DT_RowId = serializers.IntegerField(source='id')
    foo = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ['password']
    
    def get_foo(self, obj):
        return 'Hello World'


def my_view(request):
    queryset = User.objects.all()
    # You can also sort the initial data here.
    return JqueryDatatable(request, queryset, UsersSerializer, [
            {'foo': 'bar'},
    ])
```
#### b) Maping multiple columns
Previously we've discussed how you can map a field with one field present in models, but if there is a field defined in your serializer which is a combination of two or more other field and you want to map them to multiple fields, then you can use this method. <br>
For Example: <br>
If you've defined a field 'full_name' which is a combination of three field defined in your models 'first_name', 'middle_name' and 'last_name'

Models:
```python
from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=50, null=True)
    middle_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    bar = models.CharField(max_length=50, null=True)
```
Serializer and View:
```python
from django.contrib.auth.models import User
from rest_framework import serializers
from django_jquery_datatables.utils import JqueryDatatable

class UsersSerializer(serializers.ModelSerializer):
    DT_RowId = serializers.IntegerField(source='id')
    full_name = serializers.SerializerMethodField()
    foo = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ['password']
    
    def get_foo(self, obj):
        return 'Hello World'

    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.middle_name} {obj.last_name}'

def my_view(request):
    queryset = User.objects.all()
    # You can also sort the initial data here.
    return JqueryDatatable(request, queryset, UsersSerializer, [
            {'foo': 'bar'},
            {'full_name': ['first_name', 'middle_name', 'last_name']},
    ])
```

## Contributing
Contributions are welcome! If you find a bug or have a suggestion, please open an issue on the issue tracker.

If you want to contribute code, please fork the repository, create a new branch for your changes, and submit a pull request.

## License
This library is licensed under the MIT License.
