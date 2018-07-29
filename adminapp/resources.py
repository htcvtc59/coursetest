from import_export import resources
from adminapp.models import Student
from signapp.models import Account


class StudentResource(resources.ModelResource):
    class Meta:
        model = Student
        fields = (
            'fullname', 'hometown',
            'birthday', 'school',
            'graduationtime',
            'email', 'phone',
            'accountcode'
        )


class AccountResource(resources.ModelResource):
    class Meta:
        model = Account
