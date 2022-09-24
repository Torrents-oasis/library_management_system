# -*- coding:utf-8 -*-
# 防止中文注释报错
"""
author: GuoMinghao
date:   2022-05-13
"""
import os
from django.shortcuts import render, redirect, HttpResponse
from basic_func import models

from basic_func.utils.pagination import Pagination
from basic_func.utils.form import *
import random
import pandas as pd

from basic_func.views.card import get_context_dict_from_record_query


def book_delete_all(request):
    models.Book.objects.all().delete()
    return redirect('/book/list/')


def book_random_create(request):
    for i in range(5):
        name = ''.join(random.sample(
            ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f',
             'e', 'd', 'c', 'b', 'a'], random.randint(4, 8)))
        category = random.randint(1, 9)
        press = ''.join(random.sample(
            ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f',
             'e', 'd', 'c', 'b', 'a'], random.randint(1, 8)))
        year = random.randint(0, 2022)
        # author = random.sample('zyxwvutsrqponmlkjihgfedcba', random.randint(4, 8))
        author = ''.join(random.sample(
            ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f',
             'e', 'd', 'c', 'b', 'a'], random.randint(4, 8)))
        price = random.uniform(0, 99)
        total = random.randint(1, 99)
        inventory = random.randint(1, total)
        models.Book.objects.create(name=name, category=category, press=press, year=year, author=author, price=price,
                                   total=total, inventory=inventory)
    return redirect('/book/list/')


def book_create_from_excel(request):
    books_to_put_on = pd.read_excel(r'basic_func/static/file/book_info.xlsx')
    for item in books_to_put_on.index:
        info = books_to_put_on.loc[item]
        models.Book.objects.create(category=info.values[0],
                                   name=info.values[1],
                                   press=info.values[2],
                                   year=info.values[3],
                                   author=info.values[4],
                                   price=info.values[5],
                                   total=info.values[6],
                                   inventory=info.values[7])
    print("### ", os.getcwd())
    return redirect('/book/list/')


def book_list(request):
    """ 图书列表 """
    data_dict = {}
    search_data = request.GET.get('query', "")
    order_sequence = request.GET.get('order_sequence', "")
    sequence_direct = request.GET.get('sequence_direct', "")
    order_sequence = sequence_direct + order_sequence
    if order_sequence == "":
        order_sequence = "name"
    search_data_2_1 = request.GET.get('query_2_1', "")
    search_data_2_2 = request.GET.get('query_2_2', "")
    what_to_query_data = request.GET.get('what_to_query', "")
    # what_to_query_data_2 = request.GET.get('what_to_query_2', "")
    if search_data:
        # print(what_to_query_data)
        # print("### ", type(what_to_query_data))
        data_dict[what_to_query_data + "__contains"] = search_data
        # queryset = models.Book.objects.filter(**data_dict).order_by(what_to_query_data, "category")
    elif search_data_2_1 and search_data_2_2:
        num1 = int(search_data_2_1)
        num2 = int(search_data_2_2)
        data_dict[what_to_query_data + "__range"] = (num1, num2)
        # data_dict[what_to_query_data_2 + "__range"] = (num1, num2)

    queryset = models.Book.objects.filter(**data_dict).order_by(order_sequence, "category")
    page_object = Pagination(request, queryset)
    context_dict = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,  # 分页之后的数据
        "page_string": page_object.html(),  # html
        "search_data_2_1": search_data_2_1,
        "search_data_2_2": search_data_2_2,
    }
    return render(request, 'book_list.html', context_dict)


def book_add(request):
    """ 图书添加 """
    # 直接点击 /book/list/ 上的添加图书
    if request.method == "GET":
        form = BookModelForm()
        context_dict = {
            "form": form,
        }
        return render(request, 'book_add.html', context_dict)

    form = BookModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/book/list/')

    context_dict = {
        "form": form,
    }
    return render(request, 'book_add.html', context_dict)


def book_delete(request, nid):
    """ 图书删除 """
    models.Book.objects.filter(id=nid).delete()
    return redirect('/book/list/')


def book_edit(request, nid):
    """ 书籍编辑 """
    edit_object = models.Book.objects.filter(id=nid).first()

    # 进入编辑页面
    if request.method == "GET":
        form = BookEditModelForm(instance=edit_object)
        context_dict = {
            "form": form
        }
        return render(request, 'book_edit.html', context_dict)

    # 提交成功，返回list
    form = BookEditModelForm(instance=edit_object, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/book/list/')

    # 提交失败，跳回原页面
    context_dict = {
        "form": form
    }
    return render(request, 'book_edit.html', context_dict)


def book_borrow(request, nid):
    """ 书籍借阅 """
    borrow_object_query_set = models.Book.objects.filter(id=nid)
    borrow_object = borrow_object_query_set.first()

    info_dict = request.session.get("info")
    form = RecordModelForm()
    error_info = ""
    success_info = ""
    context_dict = {
        "form": form,
        "borrow_object": borrow_object,
        "info_dict": info_dict,
        "error_info": error_info,
        "success_info": success_info
    }

    # 进入借阅页面
    if request.method == "GET":
        return render(request, 'book_borrow.html', context_dict)

    # 提交成功，返回list
    form = RecordModelForm(data=request.POST)
    selected_card_id = request.POST.get('card_id')
    selected_card_object = models.Card.objects.filter(id=selected_card_id).first()
    make_appoint = False
    make_appoint = request.POST.get('make_appoint')
    make_appoint = (make_appoint == "True")

    if selected_card_object.position == 1 and borrow_object.category == 1:
        error_info = "该借书证持有人为学生, 暂无古籍借阅权限"
        context_dict = {
            "form": form,
            "borrow_object": borrow_object,
            "info_dict": info_dict,
            "error_info": error_info,
            "success_info": success_info
        }
        return render(request, 'book_borrow.html', context_dict)
    if borrow_object.inventory == 0:
        record_object = models.Record.objects.filter(book_id=nid).order_by("return_date").first()
        error_info = "该书籍暂无库存, 最近归还日期为：" + str(record_object.return_date)
        context_dict = {
            "form": form,
            "borrow_object": borrow_object,
            "info_dict": info_dict,
            "error_info": error_info,
            "success_info": success_info
        }
        # print("### ", type(make_appoint), " ### ", bool(make_appoint), "122")

        if make_appoint:
            book_select = models.Record.objects.filter(book_id=nid).first()
            if book_select.appointed:
                return HttpResponse("不能预约，已被其他人预约")
            models.Record.objects.filter(book_id=nid).update(appointed=True)

        return render(request, 'book_borrow.html', context_dict)

    if form.is_valid():
        form.save()
        borrow_object_query_set.update(inventory=borrow_object.inventory - 1)
        success_info = "借阅成功"
        context_dict = {
            "form": form,
            "borrow_object": borrow_object,
            "info_dict": info_dict,
            "error_info": error_info,
            "success_info": success_info
        }
        return render(request, 'book_borrow.html', context_dict)

        # return HttpResponse("借阅成功")

    # 提交失败，跳回原页面
    return render(request, 'book_borrow.html', context_dict)


def book_return(request, nid):
    """ 书籍归还 """
    # nid: Record - id
    record_object_query_set = models.Record.objects.filter(id=nid)
    record_object = record_object_query_set.first()

    info_dict = request.session.get("info")
    form = RecordReturnModelForm()
    error_info = ""
    success_info = ""
    context_dict = {
        "form": form,
        "record_object": record_object,
        "info_dict": info_dict,
        "error_info": error_info,
        "success_info": success_info
    }

    # 进入还书页面
    if request.method == "GET":
        return render(request, 'book_return.html', context_dict)

    # 提交成功，返回list
    form = RecordReturnModelForm(data=request.POST)
    selected_card_id = request.POST.get('card_id')
    selected_book_id = request.POST.get('book_id')
    selected_card_object_query_set = \
        models.Record.objects.filter(book_id=selected_book_id,
                                     card_id=selected_card_id,
                                     returned=False)
    if not selected_card_object_query_set.exists():
        error_info = "找不到借书记录"
        context_dict = {
            "form": form,
            "record_object": record_object,
            "info_dict": info_dict,
            "error_info": error_info,
            "success_info": success_info
        }
        return render(request, 'book_return.html', context_dict)

    selected_card_object = selected_card_object_query_set.first()

    returned_book_query_set = models.Book.objects.filter(id=selected_book_id)
    returned_book = returned_book_query_set.first()
    returned_book_query_set.update(inventory=returned_book.inventory + 1)

    models.Record.objects.filter(id=selected_card_object.id).update(returned=True)

    success_info = "书已还好"
    context_dict = {
        "form": form,
        "record_object": record_object,
        "info_dict": info_dict,
        "error_info": error_info,
        "success_info": success_info
    }
    return render(request, 'book_return.html', context_dict)

    # 提交失败，跳回原页面
    return render(request, 'book_return.html', context_dict)
