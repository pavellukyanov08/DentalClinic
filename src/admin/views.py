from flask import render_template, request, redirect, flash, url_for, Blueprint
from flask_login import current_user, login_user, logout_user, login_required

from src.users.models import Role, User
from src.users.forms import UserForm
from src.database import db
from src.views import menu

admin_page = Blueprint('admin_page', __name__)
update_user_page = Blueprint('update_user_page', __name__)
delete_user_page = Blueprint('delete_user_page', __name__)


@admin_page.route('/admin_page', methods=['GET'])
@login_required
def admin_system():
    if current_user.username == 'admin':
        users = User.query.order_by(User.id)
        roles = Role.query.order_by(Role.id)
        return render_template('admin/admin.html', users=users, roles=roles)
    else:
        flash('Вы должны иметь права администратора для доступа на эту страницу')
        return redirect(url_for('signin_user_page.signin_user'))


@update_user_page.route('/update_us/<int:idx>', methods=['GET', 'POST'])
@login_required
def update_user(idx):
    user = User.query.get_or_404(idx)
    admin_form = UserForm(obj=user)

    if request.method == 'GET':
        admin_form.email.data = user.email
        admin_form.fullname.data = user.fullname
        admin_form.username.data = user.username
        admin_form.role.data = user.role_id

    if admin_form.validate_on_submit():
        admin_form.email.data = user.email.city
        admin_form.fullname.data = user.fullname
        admin_form.username.data = user.username
        db.session.commit()
        flash('User updated successfully!')

        return redirect(url_for('admin_page.admin_system'))

    return render_template('admin/update_user.html', menus=menu, admin_form=admin_form)


@delete_user_page.route('/delete/<int:idx>', methods=['POST'])
@login_required
def delete_user(idx):
    user = User.query.get_or_404(idx)

    db.session.delete(user)
    db.session.commit()

    flash('Users deleted successfully!')
    return redirect(url_for('admin_page.admin_system'))
