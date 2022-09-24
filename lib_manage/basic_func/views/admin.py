# -*- coding:utf-8 -*-
# 防止中文注释报错
"""
author: GuoMinghao
date:   2022-05-14
"""
from django.shortcuts import render, redirect
from basic_func import models

from basic_func.utils.pagination import Pagination
from basic_func.utils.form import *


def admin_list(request):
    """ 管理员列表 """
    data_dict = {}
    search_data = request.GET.get('qurry', "")
    if search_data:
        data_dict["name__contains"] = search_data

    queryset = models.Admin.objects.filter(**data_dict).order_by("name")
    page_object = Pagination(request, queryset)
    context_dict = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,  # 分页之后的数据
        "page_string": page_object.html(),  # html
    }
    return render(request, 'admin_list.html', context_dict)


def admin_add(request):
    """ 借书证添加 """
    # return render(request, 'card_add.html')
    if request.method == "GET":
        form = AdminModelForm()
        context_dict = {
            "form": form,
        }
        return render(request, 'admin_add.html', context_dict)

    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')

    context_dict = {
        "form": form,
    }
    return render(request, 'admin_add.html', context_dict)


def admin_delete(request, nid):
    """ 借书证删除 """
    models.Admin.objects.filter(id=nid).delete()
    return redirect('/admin/list/')


def admin_edit(request, nid):
    """ 借书证编辑 """
    edit_object = models.Admin.objects.filter(id=nid).first()

    # 进入编辑页面
    if request.method == "GET":
        form = AdminEditModelForm(instance=edit_object)
        context_dict = {
            "form": form
        }
        return render(request, 'admin_edit.html', context_dict)

    # 提交成功，返回list
    form = AdminEditModelForm(instance=edit_object, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')

    # 提交失败，跳回原页面
    # print("### failed to submit")
    context_dict = {
        "form": form
    }
    return render(request, 'admin_edit.html', context_dict)


