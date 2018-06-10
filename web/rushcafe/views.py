from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import generic
from django.conf import settings

from rushcafe.forms import MenuItemForm, MenuCategoryForm
from rushcafe.models import MenuCategory, MenuItem


@login_required
def index(request):
    return render(request, 'index.html')


@login_required
def menu_categories(request):
    menu_categories = MenuCategory.objects.all()
    paginator = Paginator(menu_categories, 5)
    
    page = request.GET.get('page')
    categories = paginator.get_page(page)

    if page is None or page == '1':
        if request.user.has_perms(('rushcafe.add_menucategory',)):
            form = MenuCategoryForm()
            return render(request, 'menu/categories.html',
                        {'menu_category_list': categories, 'form': form})
    return render(request, 'menu/categories.html',
                  {'menu_category_list': categories})


@login_required
def menu_items(request):
    menu_items = MenuItem.objects.all()
    paginator = Paginator(menu_items, 5)
    
    page = request.GET.get('page')
    items = paginator.get_page(page)
    # Don't see a need to have a new item form on
    # anything other than the first page if that
    if page is None or page == '1':
        if request.user.has_perms(('rushcafe.add_menuitem',)):
            form = MenuItemForm()
            return render(request, 'menu/items.html',
                    {'menu_items_list': items, 'form': form})
    return render(request, 'menu/items.html', {'menu_items_list': items})
    

@permission_required('rushcafe.add_menucategory')
def new_menu_category(request):
    if request.method == 'POST':
        form = MenuCategoryForm(request.POST)

        if form.is_valid():
            instance = form.save()
            return redirect('menu-category', pk=instance.pk)
        return render(request, 'menu/category_new.html', {'form': form})

    form = MenuCategoryForm()

    return render(request, 'menu/category_new.html', {'form': form})


@permission_required('rushcafe.add_menuitem')
def new_menu_item(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST)

        if form.is_valid():
            instance = form.save()
            return redirect('menu-item', pk=instance.pk)
        return render(request, 'menu/item_new.html', {'form': form})

    form = MenuItemForm()
    return render(request, 'menu/item_new.html', {'form': form})


class MenuItemView(PermissionRequiredMixin, generic.DetailView):
    model = MenuItem
    permission_required = ('rushcafe.change_menuitem', 'rushcafe.delete_menuitem')


class MenuCategoryView(PermissionRequiredMixin, generic.DetailView):
    model = MenuCategory
    permission_required = ('rushcafe.change_menucategory', 'rushcafe.delete_menucategory')
