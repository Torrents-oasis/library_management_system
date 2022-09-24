from django.db import models


# Create your models here.
class Book(models.Model):
    """ 书籍 """
    category_choices = (
        (1, "古籍"),
        (2, "文学"),
        (3, "自然科学"),
        (4, "哲学、宗教"),
        (5, "社会科学"),
        (6, "医药、卫生"),
        (7, "工业技术"),
        (8, "环境科学、安全科学"),
        (9, "综合性图书"),
    )
    category = models.SmallIntegerField(verbose_name="类别", choices=category_choices)
    name = models.CharField(verbose_name="书名", max_length=64)
    press = models.CharField(verbose_name="出版社", max_length=32)
    year = models.IntegerField(verbose_name="出版年份")
    author = models.CharField(verbose_name="作者", max_length=32)
    price = models.DecimalField(verbose_name="价格", max_digits=10, decimal_places=2, default=0)
    total = models.IntegerField(verbose_name="总藏书量")
    inventory = models.IntegerField(verbose_name="当前库存")

    # def __str__(self):
    #     return self.name


class Card(models.Model):
    """ 借书证 """
    name = models.CharField(verbose_name="姓名", max_length=32)
    institution = models.CharField(verbose_name="机构", max_length=32)
    # category = models.CharField(verbose_name="类别", max_length=16)
    position_choices = (
        (1, "学生"),
        (2, "教职工"),
    )
    position = models.SmallIntegerField(verbose_name="身份", choices=position_choices)

    def __str__(self):
        return str(self.id)


class Admin(models.Model):
    """ 管理员 """
    pwd = models.CharField(verbose_name="密码", max_length=64)
    name = models.CharField(verbose_name="姓名", max_length=32)
    tel = models.CharField(verbose_name="手机号", max_length=11)

    def __str__(self):
        return self.name


class Record(models.Model):
    """ 借书记录 """
    book_id = models.ForeignKey(verbose_name="书本id", to="Book", to_field="id", null=True, blank=True,
                                on_delete=models.CASCADE)  # models.SET_NULL
    card_id = models.ForeignKey(verbose_name="借书证id", to="Card", to_field="id", null=True, blank=True,
                                on_delete=models.CASCADE)
    admin_id = models.ForeignKey(verbose_name="管理员id", to="Admin", to_field="id", null=True, blank=True,
                                 on_delete=models.CASCADE)
    lend_date = models.DateField(verbose_name="借出时间")
    return_date = models.DateField(verbose_name="还书时间")
    appointed = models.BooleanField(verbose_name="已被预约", default=False)
    returned = models.BooleanField(verbose_name="已归还", default=False)
