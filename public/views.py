# -*- coding: utf-8 -*-

import re
import os
from collections import OrderedDict

from xlutils.copy import copy
from xlrd import open_workbook

import bson
import flask

from flask import Flask, request, abort, Response, redirect, url_for, flash, Blueprint, send_from_directory
from flask.ext.mongoengine import MongoEngine
from flask.templating import render_template
from flask import make_response
from flask_security.decorators import roles_required, login_required
from user.models import User
from flask.ext.security import current_user
from mongoengine.queryset import DoesNotExist

from werkzeug import secure_filename
from settings import Config
from public.models import Product
from public.models import Menu
from public.models import Category
from public.models import MenuProduct
from public.models import Order


bp_public = Blueprint('public', __name__, static_folder='../static')


def is_food_row(row):
    if isinstance(row[0].value, float):
        return True
    return False


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in Config.ALLOWED_EXTENSIONS


def add_products_from_xls(filename):
    rb = open_workbook(filename, formatting_info=True)

    for sheet_index in xrange(5):
        sheet = rb.sheet_by_index(sheet_index)

        menu_date = re.findall(r'\d{2}.\d{2}.\d{2}', sheet.cell_value(0, 1)).pop()
        current_category = ''

        try:
            menu = Menu(date=menu_date).save()
        except flask.ext.mongoengine.mongoengine.NotUniqueError:
            menu = Menu.objects.get(date=menu_date)
            pass

        for rownum in range(sheet.nrows):
            rslc = sheet.row_slice(rownum)
            if is_food_row(rslc):
                try:
                    category = Category.objects.get(name=unicode(current_category))
                except:
                    category = Category()
                    category.name = unicode(current_category)
                    category.save()

                product = Product()
                product.name = unicode(rslc[1].value)

                weight = unicode(rslc[2].value).replace('.0', '').strip('-')
                if not weight:
                    # grammi
                    maybe_weight_is_here = re.findall(u'([0-9,]+)(\W?\u0433\u0440)', product.name)
                    if len(maybe_weight_is_here) > 0:
                        pieces = re.findall(u'\u043f\u043e\W*\d+\W*\u043f', product.name)
                        weight, description = maybe_weight_is_here.pop()
                        product.name = product.name.replace(weight + description, '')
                        weight = weight + u' \u0433'
                        weight = weight.replace(',', '.')
                        if len(pieces) > 0:
                            piece_part = u' (' + pieces.pop() + u')'
                            weight = weight + piece_part
                            product.name = product.name.replace(piece_part, '')

                    # shtuki
                    maybe_weight_is_here = re.findall(u'(\d+)(\W?\u0448\u0442)', product.name)
                    if len(maybe_weight_is_here) > 0:
                        weight, description = maybe_weight_is_here.pop()
                        product.name = product.name.replace(weight + description, '')
                        weight = weight + u' \u0448\u0442'

                    # kuski
                    maybe_weight_is_here = re.findall(u'(\d+)(\W?\u043a)', product.name)
                    if len(maybe_weight_is_here) > 0:
                        weight, description = maybe_weight_is_here.pop()
                        product.name = product.name.replace(weight + description, '')
                        weight = weight + u' \u043a'

                    # litry
                    maybe_weight_is_here = re.findall(u'([0-9,]+)(\W?\u043b)', product.name)
                    if len(maybe_weight_is_here) > 0:
                        weight, description = maybe_weight_is_here.pop()
                        product.name = product.name.replace(weight + description, '')
                        weight = weight + u' \u043b'
                        weight = weight.replace(',', '.')

                    # millylitry
                    maybe_weight_is_here = re.findall(u'([0-9,]+)(\W?\u043c\u043b)', product.name)
                    if len(maybe_weight_is_here) > 0:
                        weight, description = maybe_weight_is_here.pop()
                        product.name = product.name.replace(weight + description, '')
                        weight = weight + u' \u043c\u043b'
                        weight = weight.replace(',', '.')
                else:
                    weight = weight + u' \u0433'

                def chg_quotes(text = None):
                    if not text:
                        return
                    counter = 0
                    text = list(text)
                    for i in range(len(text)):
                        if (text[i] == u'"'):
                            counter += 1
                            if (counter % 2 == 1):
                                text[i] = u'«'
                            else:
                                text[i] = u'»'
                    return ''.join(text)

                weight = re.sub(u'(\w)(\u0448\u0442)', '\\1 \\2', weight)
                product.name = chg_quotes(product.name)
                replacements = {
                    r'\.': '',
                    r',(\W)': ', \\1',
                    r'[,. ]+$': '',
                    u'Шоколад «Аленка» с начинкой Вареная сгущенка': u'Шоколад «Алёнка» с варёной сгущёнкой',
                    u'Щи Щавелевые с яйцом': u'Щи щавелевые с яйцом',
                    u'Лапша Грибная домашняя': u'Лапша грибная домашняя',
                    u'Суп Фасолевый с говядиной': u'Суп фасолевый с говядиной',
                    u'Борщ «Украинский» с курицей': u'Борщ украинский с курицей',
                    u'Суп Рыбный': u'Суп рыбный',
                    u'ПАСТА Таглиателли с курицей в сырном соусе': u'Паста таглиателли с курицей в сырном соусе',
                    u'Лапша пшеничная удон с курицей, бульоном и яйцом': u'Лапша пшеничная удон (курица, бульон и яйцо)'
                }

                for was, then in replacements.iteritems():
                    product.name = re.sub(was, then, product.name)

                compounds = re.findall(r'\(\W+\)', product.name)
                if len(compounds) > 0:
                    compound = compounds.pop()
                    product.compound = re.sub(r'\((\W+)\)', '\\1', compound)
                    product.name = product.name.replace(compound, '')

                product.weight = weight
                product.cost = int(rslc[3].value)
                product.category = category

                try:
                    product.save()
                except flask.ext.mongoengine.mongoengine.NotUniqueError:
                    product = Product.objects.get(name=product.name,
                                                  weight=product.weight,
                                                  cost=product.cost)
                except bson.errors.InvalidBSON:
                    continue

                pmconnection = MenuProduct()
                pmconnection.menu = menu
                pmconnection.product = product
                try:
                    pmconnection.save()
                except flask.ext.mongoengine.mongoengine.NotUniqueError:
                    continue
            else:
                current_category = rslc[0].value


@bp_public.route('/')
def index():
    return render_template('index.html')


@bp_public.route('/robots.txt')
def static_from_root():
    return send_from_directory(bp_public.static_folder, request.path[1:])


@bp_public.route('/order', methods=['POST'])
@login_required
def order():
    product_id = request.values.get('product')
    menu_id = request.values.get('menu')

    try:
        menu = Menu.objects.get(id=menu_id)
    except DoesNotExist:
        pass

    try:
        product = Product.objects.get(id=product_id)
    except DoesNotExist:
        pass

    try:
        order = Order.objects.get(menu=menu, product=product)
        order.count += 1
        order.save()
    except DoesNotExist:
        order = Order()
        order.menu = menu
        order.product = product
        order.user = User.objects.get(id=current_user.id)
        order.save()

    return render_template('order.html',
                           count=order.count)


@bp_public.route('/cancel', methods=['POST'])
@login_required
def cancel():
    product_id = request.values.get('product')
    menu_id = request.values.get('menu')

    try:
        menu = Menu.objects.get(id=menu_id)
    except DoesNotExist:
        pass

    try:
        product = Product.objects.get(id=product_id)
    except DoesNotExist:
        pass

    try:
        order = Order.objects.get(menu=menu, product=product)
        order.delete()
    except DoesNotExist:
        pass

    return render_template('order.html',
                           count=0)


@bp_public.route('/menu')
@login_required
def view_menu():
    menu = Menu.objects(date='2015-11-24').first()
    all_products = MenuProduct.objects.filter(menu=menu).values_list('product').all_fields()
    ordered_products = Order.objects.filter(product__in=all_products, menu=menu).all_fields()

    products = OrderedDict()
    for product in all_products:
        order_count = 0
        for order in ordered_products:
            if order.product == product:
                order_count = order.count
                break

        if not products.get(product.category.name):
            products[product.category.name] = []

        products[product.category.name].append({
            'id': product.id,
            'category_id': product.category.id,
            'name': product.name,
            'weight': product.weight,
            'cost': product.cost,
            'compound': product.compound,
            'count': order_count,
        })

    return render_template('viewmenu.html', products=products, menu_id=menu.id)

@bp_public.route('/loadmenu', methods=['GET', 'POST'])
@login_required
def load_menu():
    if request.method == 'GET':
        return render_template('loadmenu.html')
    elif request.method == 'POST':
        menu = request.files['menu']
        if menu and allowed_file(menu.filename):
            filename = secure_filename(menu.filename)
            path = os.path.join(Config.UPLOAD_FOLDER, filename)
            menu.save(path)
            try:
                add_products_from_xls(path)
            except IndexError:
                return render_template('loadmenu.html', status='error')
            return render_template('loadmenu.html', status='success')
        else:
            return render_template('loadmenu.html', status='error')
