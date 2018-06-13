from decimal import Decimal, InvalidOperation

from rushcafe.models import MenuCategory, MenuItem


def get_category(req):
    try:
        category_param = req['queryResult']['parameters']['menu-category']
    except KeyError:
        return None
    category = MenuCategory.objects.filter(name__contains=category_param, deleted=False).first()
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

    print(req)

    action = req['queryResult']['action']
    message = "Can't help sorry"

    if action == 'get-menu-categories':
        result_data = [c.name for c in MenuCategory.objects.filter(deleted=False)]
        message = 'We have the following categories on our menu: ' + ', '.join(result_data)
        print(message)
    elif action == 'get-menu-items':
        result_data = [i.name for i in get_menu_items()]
        message = 'We have the following options on our menu: ' + ', '.join(result_data)
    elif action == 'get-items-in-category':
        category = get_category(req)
        if category:
            result_data = [i.name for i in get_menu_items(category=category)]
            message = 'We have the following options in {0}: '.format(category.name) + ', '.join(result_data)
        else:
            message = 'We don\'t have that category on our menu, sorry'
    elif action == 'get-cheapest-item':
        menu_item = MenuItem.objects.filter(deleted=False).order_by('price').first()
        if menu_item:
            message = '{0} is our cheapest item on the menu at ${1}'.format(menu_item.name, menu_item.price)
        else:
            message = 'We have nothing on our menu'
    elif action == 'menu-items-under-price':
        amount = get_param_amount(req)
        category = get_category(req)

        if amount is not None and amount is not '':
            menu_items = [i.name for i in get_menu_items(category=category, less_than_price=amount)]
            if menu_items:
                message = ('The following options are under ${0}: '
                           ''.format(amount) + ', '.join(menu_items))
            else:
                message = 'I\'m sorry, we have nothing under ${0}'.format(amount)
        else:
            message = "Sorry, could you try being more specific"

    return message
