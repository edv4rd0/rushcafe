from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.shortcuts import (get_object_or_404, redirect, render,
                              render_to_response, reverse)
from django.template import RequestContext
from django.views.generic.edit import UpdateView

from rushcafe.forms import DeleteForm, MenuCategoryForm, MenuItemForm
from rushcafe.models import MenuCategory, MenuItem


@login_required
def index(request):
    return render(request, 'index.html')


@login_required
def menu_categories(request):
    menu_categories = MenuCategory.objects.filter(deleted=False)
    paginator = Paginator(menu_categories, 5)
    
    page = request.GET.get('page')
    categories = paginator.get_page(page)

    if page is None or page == '1':
        if request.user.has_perms(('rushcafe.add_menucategory',)):
            form = MenuCategoryForm()
            return render(request, 'rushcafe/categories.html',
                        {'menu_category_list': categories, 'form': form})
    return render(request, 'rushcafe/categories.html',
                  {'menu_category_list': categories})


@login_required
def menu_items(request):
    menu_items = MenuItem.objects.filter(deleted=False)
    paginator = Paginator(menu_items, 5)
    
    page = request.GET.get('page')
    items = paginator.get_page(page)
    # Don't see a need to have a new item form on
    # anything other than the first page if that
    if page is None or page == '1':
        if request.user.has_perms(('rushcafe.add_menuitem',)):
            form = MenuItemForm()
            return render(request, 'rushcafe/items.html',
                    {'menu_items_list': items, 'form': form})
    return render(request, 'rushcafe/items.html', {'menu_items_list': items})
    

@permission_required('rushcafe.add_menucategory')
def new_menu_category(request):
    if request.method == 'POST':
        form = MenuCategoryForm(request.POST)

        if form.is_valid():
            instance = form.save()
            return redirect('menu-category', pk=instance.pk)
        return render(request, 'rushcafe/category_new.html', {'form': form})

    form = MenuCategoryForm()

    return render(request, 'rushcafe/category_new.html', {'form': form})


@permission_required('rushcafe.delete_menucategory')
def delete_menu_category(request, pk):
    menu_category = get_object_or_404(MenuCategory, pk=pk)
    if request.method == 'POST':
        form = DeleteForm(request.POST)
        if form.is_valid():
            print("Is valid")
            menu_category.deleted = form.cleaned_data['deleted']
            print(menu_category.deleted)
            menu_category.save()
            return redirect('menu-categories')
        return redirect('menu-category', pk=menu_category.pk)
    
    form = DeleteForm({'deleted': menu_category.deleted})
    return render(request, 'rushcafe/menucategory_delete.html', {'form': form, 'menucategory': menu_category})


@permission_required('rushcafe.add_menuitem')
def new_menu_item(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST)

        if form.is_valid():
            instance = form.save()
            return redirect('menu-item', pk=instance.pk)
        return render(request, 'rushcafe/item_new.html', {'form': form})

    form = MenuItemForm()
    return render(request, 'rushcafe/item_new.html', {'form': form})


@permission_required('rushcafe.delete_menuitem')
def delete_menu_item(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        form = DeleteForm(request.POST)

        if form.is_valid():
            menu_item.deleted = form.cleaned_data['deleted']
            menu_item.save()
            return redirect('menu-items')
        return redirect('menu-item', pk=pk)

    form = DeleteForm({'deleted': menu_item.deleted})
    return render(request, 'rushcafe/menuitem_delete.html', {'form': form, 'menuitem': menu_item})


class MenuItemView(PermissionRequiredMixin, UpdateView):
    model = MenuItem
    permission_required = ('rushcafe.change_menuitem', 'rushcafe.delete_menuitem')
    form_class = MenuItemForm

    def get_initial(self):
        return { 'category' : self.object.category.id }
    
    def get_success_url(self):
        return reverse('menu-item', kwargs={'pk': self.object.id})


class MenuCategoryView(PermissionRequiredMixin, UpdateView):
    model = MenuCategory
    permission_required = ('rushcafe.change_menucategory', 'rushcafe.delete_menucategory')
    fields = ['name']

    def get_success_url(self):
        return reverse('menu-category', kwargs={'pk': self.object.id})

def handler404(request, exception, template_name='404.html'):
    response = render_to_response(template_name, context=RequestContext(request))
    response.status_code = 404
    return response
