from flask import Flask, redirect, url_for, render_template, request, flash
from models import db, Contact, User
from forms import ContactForm
from flask_login import LoginManager, current_user, login_user, login_required


# Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'my secret'
app.config['DEBUG'] = False

# Database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/hp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Login
login_manager = LoginManager()
login_manager.init_app(app)
password = 'sintow2020@'


@login_manager.user_loader    
#使用user_loader装饰器的回调函数非常重要，他将决定 user 对象是否在登录状态
def user_loader(id):          
    #这个id参数的值是在 login_user(user)中传入的 user 的 id 属性
    user = User()
    return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
        <form action="#" method="POST">
            <span>请输入账号</span>
            <input type="text" name="name" id="name" placeholder="name">
            <span>请输入密码</span>
            <input type="password" name="pw" id="pw" placeholder="password">
            <input type="submit" name="submit">
       </form>
        '''
    name = request.form.get('name')
    if request.form.get('pw') == password:
        user = User()
        login_user(user)
        return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route("/")
@login_required
def index():
    '''
    Home page
    '''
    return redirect(url_for('contacts'))


@app.route("/new_contact", methods=('GET', 'POST'))
@login_required
def new_contact():
    '''
    Create new contact
    '''
    form = ContactForm()
    if form.validate_on_submit():
        my_contact = Contact()
        form.populate_obj(my_contact)
        db.session.add(my_contact)
        try:
            db.session.commit()
            # User info
            flash('Contact created correctly', 'success')
            return redirect(url_for('contacts'))
        except Exception as ex:
            db.session.rollback()
            flash('Error generating contact. {}'.format(ex), 'danger')

    return render_template('web/new_contact.html', form=form)


@app.route("/edit_contact/<id>", methods=('GET', 'POST'))
@login_required
def edit_contact(id):
    '''
    Edit contact

    :param id: Id from contact
    '''
    my_contact = Contact.query.filter_by(id=id).first()
    form = ContactForm(obj=my_contact)
    if form.validate_on_submit():
        try:
            # Update contact
            form.populate_obj(my_contact)
            db.session.add(my_contact)
            db.session.commit()
            # User info
            flash('Saved successfully', 'success')
        except:
            db.session.rollback()
            flash('Error update contact.', 'danger')
    return render_template(
        'web/edit_contact.html',
        form=form)


@app.route("/contacts")
@login_required
def contacts():
    '''
    Show alls contacts
    '''
    contacts = Contact.query.order_by(Contact.name).all()
    return render_template('web/contacts.html', contacts=contacts)


@app.route("/search")
@login_required
def search():
    '''
    Search
    '''
    name_search = request.args.get('name')
    all_contacts = Contact.query.filter(
        Contact.name.contains(name_search)
        ).order_by(Contact.name).all()
    return render_template('web/contacts.html', contacts=all_contacts)


@app.route("/contacts/delete", methods=('POST',))
@login_required
def contacts_delete():
    '''
    Delete contact
    '''
    try:
        mi_contacto = Contact.query.filter_by(id=request.form['id']).first()
        db.session.delete(mi_contacto)
        db.session.commit()
        flash('Delete successfully.', 'danger')
    except:
        db.session.rollback()
        flash('Error delete  contact.', 'danger')

    return redirect(url_for('contacts'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
