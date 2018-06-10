from django.contrib.auth.models import Group, Permission, User
from django.test import TestCase
from django.urls import reverse

from rushcafe.forms import MenuCategoryForm, MenuItemForm
from rushcafe.models import MenuCategory, MenuItem


class MenuTestCase(TestCase):
    """Tests for the Cafe Menu CMS"""
    def setUp(self):
        mc = MenuCategory.objects.create(name="Starters")
        mi = MenuItem.objects.create(name="Burger and Fries", price=12.99, category=mc)

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='cmsadmin')
        user.set_password('pass@123')
        permissions = Permission.objects.filter(content_type__app_label='rushcafe')
        group = Group(name='cafecms')
        group.save()
        group.permissions.set(permissions)
        
        user.groups.add(group)
        user.save()

        # setup second user with no perms
        user = User.objects.create(username='noperms')
        user.set_password('pass@123')
        user.save()

    def test_index(self):
        """The main dashboard should load correctly"""
        self.client.login(username='cmsadmin', password='pass@123')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_index_redirect(self):
        """The main dashboard should redirect to login page if not logged in"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             '{0}?next={1}'.format(reverse('login'),
                                                   reverse('index')),
                             status_code=302, target_status_code=200)

    def test_add_item(self):
        """Test a get request to the add menu item view with
        cmsadmin user and appropriate permissions"""
        self.client.login(username='cmsadmin', password='pass@123')
        response = self.client.get(reverse('menu-item-add'))
        self.assertEqual(response.status_code, 200)

    def test_add_item_bad_permissions(self):
        """Tests GET request to add item page with logged in user and no permissions"""
        self.client.login(username='noperms', password='pass@123')
        response = self.client.get(reverse('menu-item-add'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             '{0}?next={1}'.format(reverse('login'),
                                                   reverse('menu-item-add')),
                             status_code=302, target_status_code=200)

    def test_item_form(self):
        """Test the form"""
        form_data = {'name': 'Cheesecake', 'category': 1, 'price': 17.99}
        form = MenuItemForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_item_form_bad_category(self):
        """Test using non-existent category"""
        form_data = {'name': 'Cheesecake', 'category': 2, 'price': 17.99}
        form = MenuItemForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_category_form(self):
        """Test the form"""
        form_data = {'name': 'Mains'}
        form = MenuCategoryForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_add_item_post(self):
        """Item should be added and user redirected to item details view"""
        self.client.login(username='cmsadmin', password='pass@123')
        form_data = {'name': 'Cheesecake', 'category': 1, 'price': 17.99}
        response = self.client.post(reverse('menu-item-add'), form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('menu-item', kwargs={'pk': 2}),
                             status_code=302, target_status_code=200)
    
    def test_item_details(self):
        """Item should be retrieved and the name should be in the template.
        XXX: Future tests should be more involved, such as using selenium"""
        self.client.login(username='cmsadmin', password='pass@123')
        response = self.client.get(reverse('menu-item', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rushcafe/menuitem_form.html')
        self.assertContains(response, 'Burger and Fries')

    def test_item_details_post(self):
        """Endpoint does not handle creation"""
        self.client.login(username='cmsadmin', password='pass@123')
        form_data = {'name': 'Cheesecake', 'category': 1, 'price': 17.99}
        response = self.client.post(reverse('menu-item', kwargs={'pk': 7}), form_data)
        self.assertEqual(response.status_code, 404)

    def test_category_details(self):
        """Category should be retrieved and the name should be in the template.
        XXX: Future tests should be more involved, such as using selenium"""
        self.client.login(username='cmsadmin', password='pass@123')
        response = self.client.get(reverse('menu-category', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rushcafe/menucategory_form.html')
        self.assertContains(response, 'Starters')

    def test_category_details_post(self):
        """Endpoint does not handle creation"""
        self.client.login(username='cmsadmin', password='pass@123')
        form_data = {'name': 'Sides'}
        response = self.client.post(reverse('menu-category', kwargs={'pk': 7}), form_data)
        self.assertEqual(response.status_code, 404)
