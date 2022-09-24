from basic_func import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django import forms
from basic_func.utils.bootstrap import BootStrapModelForm
from datetime import datetime
from dateutil import relativedelta


# class UserModelForm(BootStrapModelForm):
#     name = forms.CharField(
#         min_length=3,
#         label="用户名",
#         widget=forms.TextInput(attrs={"class": "form-control"})
#     )
#
#     class Meta:
#         model = models.UserInfo
#         fields = ["name", "password", "age", 'account', 'create_time', "gender", "depart"]

class AdminModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = "__all__"
        exclude = []

    # 验证
    def clean_name(self):
        # 验证名字
        admin_name = self.cleaned_data["name"]
        exists = models.Admin.objects.filter(name=admin_name).exists()
        if exists:
            raise ValidationError("该管理员已存在")
        return admin_name

    def clean_tel(self):
        # 验证电话号码
        tel_number = self.cleaned_data["tel"]
        # print(" ### tel_number: {} 1".format(tel_number))
        if len(tel_number) != 11 or tel_number[0] != '1' or tel_number[1] == '2':
            raise ValidationError("电话号码格式不正确")
        return tel_number


class AdminEditModelForm(BootStrapModelForm):
    name = forms.CharField(
        label="姓名",
    )

    class Meta:
        model = models.Admin
        fields = "__all__"

    # 验证
    def clean_name(self):
        # print(self.instance.pk)
        admin_name = self.cleaned_data["name"]
        exists = models.Admin.objects.exclude(id=self.instance.pk).filter(name=admin_name).exists()
        if exists:
            raise ValidationError("该管理员已存在，请勿重复添加")

        # 验证通过，用户输入的值返回
        return admin_name

    def clean_tel(self):
        # 验证电话号码
        tel_number = self.cleaned_data["tel"]
        # print(" ### tel_number: {} 1".format(tel_number))
        if len(tel_number) != 11 or tel_number[0] != '1' or tel_number[1] == '2':
            raise ValidationError("电话号码格式不正确")
        return tel_number


class CardModelForm(BootStrapModelForm):
    class Meta:
        model = models.Card
        fields = "__all__"
        exclude = []

    # 验证
    def clean_name(self):
        user_name = self.cleaned_data["name"]

        exists = models.Card.objects.filter(name=user_name).exists()
        if exists:
            raise ValidationError("该用户已注册借书证")
        # 未注册过，返回输入姓名
        return user_name


class CardEditModelForm(BootStrapModelForm):
    name = forms.CharField(
        label="姓名",
    )

    class Meta:
        model = models.Card
        fields = "__all__"

    # 验证
    def clean_name(self):
        # print(self.instance.pk)
        user_name = self.cleaned_data["name"]
        exists = models.Card.objects.exclude(id=self.instance.pk).filter(name=user_name).exists()
        if exists:
            raise ValidationError("该用户已存在借书证，请勿重复办理")

        # 验证通过，用户输入的值返回
        return user_name


class BookModelForm(BootStrapModelForm):
    class Meta:
        model = models.Book
        fields = "__all__"
        exclude = []

    # 验证书名是否存在
    def clean_name(self):
        book_name = self.cleaned_data["name"]

        exists = models.Book.objects.filter(name=book_name).exists()
        if exists:
            raise ValidationError("该书已存在")
        return book_name

    def clean_inventory(self):
        book_inventory = self.cleaned_data["inventory"]
        book_total = self.cleaned_data["total"]

        if book_total < book_inventory:
            raise ValidationError("当前库存不能大于总藏书量")
        return book_inventory


class BookEditModelForm(BootStrapModelForm):
    name = forms.CharField(
        label="书名",
    )

    # press = forms.CharField(
    #     label="出版社",
    # )

    class Meta:
        model = models.Book
        fields = "__all__"

    # 验证
    def clean_name(self):
        # print(self.instance.pk)
        book_name = self.cleaned_data["name"]
        # book_press = self.cleaned_data["press"]
        exists = models.Book.objects.exclude(id=self.instance.pk).filter(name=book_name).exists()
        # exists = models.Book.objects.exclude(id=self.instance.pk).filter(name=book_name, press=book_press).exists()
        # exists = models.Book.objects.exclude(id=self.instance.pk).filter(name=book_name).filter(press=book_press).exists()
        if exists:
            raise ValidationError("该书籍已存在，请勿重复添加")

        # 验证通过，用户输入的值返回
        return book_name

    def clean_inventory(self):
        book_inventory = self.cleaned_data["inventory"]
        book_total = self.cleaned_data["total"]

        if book_total < book_inventory:
            raise ValidationError("当前库存不能大于总藏书量")
        return book_inventory


class RecordModelForm(BootStrapModelForm):
    # selected_book_id = 0

    # def __init__(self, selected_book_info):
    #     self.selected_book_id = selected_book_info.id

    # book_id = forms.CharField(
    #     label="书籍id",
    #     # initial="id",
    #     widget=forms.TextInput(attrs={"class": "form-control"})
    # )
    #
    # admin_id = forms.CharField(
    #     label="管理员id",
    #     widget=forms.TextInput(attrs={"class": "form-control"})
    # )

    lend_date = forms.DateField(
        label="借出日期",
        initial=datetime.now,
    )

    return_date = forms.DateField(
        label="还书日期",
        # initial=datetime.now + datetime.month
        # initial=datetime.timedelta(days=30),
        initial=datetime.now() + relativedelta.relativedelta(months=1)
    )

    class Meta:
        model = models.Record
        # fields = "__all__"
        exclude = ["appointed"]

    # 验证书名是否存在
    def clean_name(self):
        book_id = self.cleaned_data["book_id"]
        return book_id

    def clean_name(self):
        admin_id = self.cleaned_data["admin_id"]
        return admin_id


class RecordReturnModelForm(BootStrapModelForm):
    class Meta:
        model = models.Record
        fields = ["book_id", "card_id"]


class RecordEditModelForm(BootStrapModelForm):
    name = forms.CharField(
        label="书名",
    )

    # press = forms.CharField(
    #     label="出版社",
    # )

    class Meta:
        model = models.Book
        fields = "__all__"

    # 验证
    def clean_name(self):
        # print(self.instance.pk)
        book_name = self.cleaned_data["name"]
        # book_press = self.cleaned_data["press"]
        exists = models.Book.objects.exclude(id=self.instance.pk).filter(name=book_name).exists()
        # exists = models.Book.objects.exclude(id=self.instance.pk).filter(name=book_name, press=book_press).exists()
        # exists = models.Book.objects.exclude(id=self.instance.pk).filter(name=book_name).filter(press=book_press).exists()
        if exists:
            raise ValidationError("该书籍已存在，请勿重复添加")

        # 验证通过，用户输入的值返回
        return book_name

    def clean_inventory(self):
        book_inventory = self.cleaned_data["inventory"]
        book_total = self.cleaned_data["total"]

        if book_total < book_inventory:
            raise ValidationError("当前库存不能大于总藏书量")
        return book_inventory
