# -*- coding:utf-8 -*-
# 防止中文注释报错
"""
author: GuoMinghao
date:   2022-05-13
"""
from django.db.models import Prefetch
from django.http import HttpResponse
from django.shortcuts import render, redirect
from basic_func import models

from basic_func.utils.pagination import Pagination
from basic_func.utils.form import *


def card_list(request):
    """ 借书证列表 """
    data_dict = {}
    search_data = request.GET.get('qurry', "")
    if search_data:
        data_dict["name__contains"] = search_data

    queryset = models.Card.objects.filter(**data_dict).order_by("name")
    page_object = Pagination(request, queryset)
    context_dict = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,  # 分页之后的数据
        "page_string": page_object.html(),  # html
    }
    return render(request, 'card_list.html', context_dict)


def card_add(request):
    """ 借书证添加 """
    # return render(request, 'card_add.html')
    if request.method == "GET":
        form = CardModelForm()
        context_dict = {
            "form": form,
        }
        return render(request, 'card_add.html', context_dict)

    form = CardModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/card/list/')

    context_dict = {
        "form": form,
    }
    return render(request, 'card_add.html', context_dict)


def card_delete(request, nid):
    """ 借书证删除 """
    query_set = models.Record.objects.filter(card_id=nid).exists()
    if query_set:
        return HttpResponse("该图书证存在尚未归还的图书馆，不能删除")
    models.Card.objects.filter(id=nid).delete()
    return redirect('/card/list/')


def card_edit(request, nid):
    """ 借书证编辑 """
    edit_object = models.Card.objects.filter(id=nid).first()

    # 进入编辑页面
    if request.method == "GET":
        form = CardEditModelForm(instance=edit_object)
        context_dict = {
            "form": form
        }
        return render(request, 'card_edit.html', context_dict)

    # 提交成功，返回list
    form = CardEditModelForm(instance=edit_object, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/card/list/')

    # 提交失败，跳回原页面
    # print("### failed to submit")
    context_dict = {
        "form": form
    }
    return render(request, 'card_edit.html', context_dict)


def get_context_dict_from_record_query(request):
    """ 用于以下函数的代码复用
    record_query(request)，
    record_expand(request, nid)，
    record_return(request, nid)，
    record_delete(request, nid)"""
    search_data = request.GET.get('query', "")
    # print("### ", search_data)
    queryset = models.Record.objects.filter(card_id=search_data).order_by("-returned", "lend_date")
    # queryset = models.Record.objects.filter(book_id=search_data).order_by("-returned", "lend_date")

    # record_book = models.Record.objects.filter(card_id=search_data).select_related('book_id')
    record_book = queryset.select_related('book_id')
    # print("type(record_book): ", type(record_book))
    # for item in record_book:
    #     print(item.book_id.name)

    # page_object = Pagination(request, queryset)
    page_object = Pagination(request, record_book)
    context_dict = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,  # 分页之后的数据
        "page_string": page_object.html(),  # html
    }

    return context_dict


def record_query(request):
    """ 借书记录列表 """
    # search_data = request.GET.get('query', "")
    context_dict = get_context_dict_from_record_query(request)
    return render(request, 'record_list.html', context_dict)


def record_expand(request, nid):
    """ 借书记录延长一个月 """
    record_item_query_set = models.Record.objects.filter(id=nid)
    record_item = record_item_query_set.first()
    # print("### ", record_item.return_date)
    # 更新到一个月后
    record_item_query_set.update(
        return_date=record_item.return_date + relativedelta.relativedelta(months=1))

    context_dict = get_context_dict_from_record_query(request)
    return render(request, 'record_list.html', context_dict)


def record_return(request, nid):
    """ 借书记录 - 还书 """
    record_item_query_set = models.Record.objects.filter(id=nid)
    record_item = record_item_query_set.first()
    # print("### ", record_item.return_date)
    if record_item.returned:
        return HttpResponse("该书已归还，请勿重复还书")

    borrow_object_query_set = models.Book.objects.filter(id=nid)
    borrow_object = borrow_object_query_set.first()
    borrow_object_query_set.update(inventory=borrow_object.inventory + 1)

    record_item_query_set.update(returned=True)

    context_dict = get_context_dict_from_record_query(request)
    return render(request, 'record_list.html', context_dict)


def record_delete(request, nid):
    """ 删除借书记录 """
    models.Record.objects.filter(id=nid).delete()

    context_dict = get_context_dict_from_record_query(request)
    return render(request, 'record_list.html', context_dict)
