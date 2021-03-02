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
password = '123456'


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

@app.route("/test1", methods=('GET', 'POST'))
@login_required
def test1():
    c1 = dict()
    c1['account'] = '15120201012'
    c1['ip'] = '23.14.234.12'
    c1['location'] = '河南郑州'
    c1['isp'] = '中国联通'
    c1['cnt1'] = '3'
    c1['cnt2'] = '2'

    c2 = dict()
    c2['account'] = '15120210128'
    c2['ip'] = '12.221.21.2'
    c2['location'] = '广州深圳'
    c2['isp'] = '中国联通'
    c2['cnt1'] = '1'
    c2['cnt2'] = '1'

    c3 = dict()
    c3['account'] = '15220201214'
    c3['ip'] = '122.23.11.25'
    c3['location'] = '北京'
    c3['isp'] = '中国电信'
    c3['cnt1'] = '8'
    c3['cnt2'] = '4'

    data = []
    data.append(c1)
    data.append(c2)
    data.append(c3)

    return render_template('web/test1.html', contacts=data)

@app.route("/test2", methods=('GET', 'POST'))
@login_required
def test2():

    t1 = dict()
    t1['account'] = '15220201027'
    t1['login'] = '2021-02-28 12:16:23'
    t1['duration'] = '41'
    t1['total'] = '953'

    t2 = dict()
    t2['account'] = '15220201214'
    t2['login'] = '2021-02-22 09:23:51'
    t2['duration'] = '342'
    t2['total'] = '1234'

    t3 = dict()
    t3['account'] = '15220210129'
    t3['login'] = '2020-12-31 12:34:22'
    t3['duration'] = '12'
    t3['total'] = '31'

    t4 = dict()
    t4['account'] = '15320201030'
    t4['login'] = '2021-01-03 20:12:34'
    t4['duration'] = '434'
    t4['total'] = '1356'

    data = []
    data.append(t1)
    data.append(t2)
    data.append(t3)
    data.append(t4)

    return render_template('web/test2.html', contacts=data)

@app.route("/test3", methods=('GET', 'POST'))
@login_required
def test3():

    d1 = dict()
    d1['account'] = '15220210129'
    d1['count'] = 9

    d2 = dict()
    d2['account'] = '15320201013'
    d2['count'] = 22

    d3 = dict()
    d3['account'] = '15320210302'
    d3['count'] = 78

    d4 = dict()
    d4['account'] = '15220210129'
    d4['count'] = 12

    data = []
    data.append(d1)
    data.append(d2)
    data.append(d3)
    data.append(d4)

    return render_template('web/test3.html', contacts=data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
