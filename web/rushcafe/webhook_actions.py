import string
from decimal import Decimal, InvalidOperation

from rushcafe.models import MenuCategory, MenuItem


translator = str.maketrans('', '', string.punctuation)


def get_category(req):
    try:
        category_param = req['queryResult']['parameters']['menu-category']
    except KeyError:
        return None
    category = MenuCategory.objects.filter(name__contains=category_param.translate(translator), deleted=False).first()
    return category


def get_param_amount(json_dict):
    try:
        amount = Decimal(json_dict['queryResult']['parameters']['unit-currency']['amount'])
    except (TypeError, InvalidOperation):
        try:
            amount = json_dict['queryResult']['parameters']['number']
        except (TypeError, InvalidOperation, KeyError):
            amount = None
    return amount


def get_menu_items(category=None, less_than_price=None):
    menu_items = MenuItem.objects.filter(deleted=False)
    if category is not None:
        menu_items = menu_items.filter(category=category)
    if less_than_price is not None:
        menu_items = menu_items.filter(price__lt=less_than_price)
    return menu_items


def get_action_response(req):
    """Determine the action requested by DialogFlow and respond with 
    data and message.
    
    Really need to refactor with the text strings out."""

    action = req['queryResult']['action']
    message = "Can't help sorry"

    if action == 'get-menu-categories':
        result_data = [c.name for c in MenuCategory.objects.filter(deleted=False)]
        if result_data:
            return 'We have the following categories on our menu: ' + ', '.join(result_data)
        return 'A cafe with no menu!'
    elif action == 'get-menu-items':
        result_data = [i.name for i in get_menu_items()]
        if result_data:
            return 'We have the following options on our menu: ' + ', '.join(result_data)
        return 'No options on our menu sorry'
    elif action == 'get-items-in-category':
        category = get_category(req)
        if category:
            result_data = [i.name for i in get_menu_items(category=category)]
            if result_data:
                return 'We have the following options in {0}: '.format(category.name) + ', '.join(result_data)
            return 'No options under that menu category, sorry'
        return 'We don\'t have that category on our menu, sorry'
    elif action == 'get-cheapest-item':
        menu_item = MenuItem.objects.filter(deleted=False).order_by('price').first()
        if menu_item:
            return '{0} is our cheapest item on the menu at ${1}'.format(menu_item.name, menu_item.price)
        return 'We have nothing on our menu'
    elif action == 'menu-items-under-price':
        amount = get_param_amount(req)
        category = get_category(req)

        if amount is not None and amount is not '':
            menu_items = [i.name for i in get_menu_items(category=category, less_than_price=amount)]
            if menu_items:
                if category:
                    return ('The following options in {0} are under ${1}: '
                           ''.format(category.name, amount) + ', '.join(menu_items))
                return ('The following options are under ${0}: '
                        ''.format(amount) + ', '.join(menu_items))
            else:
                return 'I\'m sorry, we have nothing under ${0}'.format(amount)
        else:
            return "Sorry, could you try being more specific"

    return message
