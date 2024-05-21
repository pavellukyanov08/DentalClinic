# Navigation menu database. Using in users, clinic and admin views

menu = [
    {'name': 'База клиентов', 'url': '/clients'},
    {'name': 'База врачей', 'url': '/doctors'},

    {'name': 'Добавить клиента', 'url': '/add_client'},
    {'name': 'Добавить врача', 'url': '/add_doctor'},

    {'name': 'Регистрация', 'url': '/signup'},
    {'name': 'Авторизация', 'url': '/signin'},
    {'name': 'Выйти', 'url': '/logout'},
]

# nav_menu = menu[:4]
# auth_menu = menu[4:]