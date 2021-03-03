from flask import Flask, redirect, url_for, render_template, request, flash
from models import db, Contact, User
from forms import ContactForm
from flask_login import LoginManager, current_user, login_user, login_required
import requests, random


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

# master
all_city = [u'\u5e7f\u5dde', u'\u4f5b\u5c71', u'\u6e5b\u6c5f', u'\u73e0\u6d77', u'\u8087\u5e86', u'\u4e1c\u839e',
        u'\u60e0\u5dde', u'\u4e2d\u5c71', u'\u8302\u540d', u'\u6c55\u5934', u'\u6885\u5dde', u'\u97f6\u5173',
        u'\u6c5f\u95e8', u'\u6e05\u8fdc', u'\u6f6e\u5dde', u'\u9633\u6c5f', u'\u6cb3\u6e90', u'\u63ed\u9633',
        u'\u6c55\u5c3e', u'\u4e91\u6d6e', u'\u6df1\u5733', u'\u4e1c\u57ce\u533a', u'\u897f\u57ce\u533a',
        u'\u671d\u9633\u533a', u'\u4e30\u53f0\u533a', u'\u77f3\u666f\u5c71\u533a', u'\u6d77\u6dc0\u533a',
        u'\u95e8\u5934\u6c9f\u533a', u'\u623f\u5c71\u533a', u'\u901a\u5dde\u533a', u'\u987a\u4e49\u533a',
        u'\u660c\u5e73\u533a', u'\u5927\u5174\u533a', u'\u6000\u67d4\u533a', u'\u5e73\u8c37\u533a',
        u'\u5bc6\u4e91', u'\u5ef6\u5e86', u'\u6d66\u4e1c\u65b0\u533a', u'\u5f90\u6c47\u533a',
        u'\u957f\u5b81\u533a', u'\u666e\u9640\u533a', u'\u95f8\u5317\u533a', u'\u8679\u53e3\u533a',
        u'\u6768\u6d66\u533a', u'\u9ec4\u6d66\u533a', u'\u9759\u5b89\u533a', u'\u5b9d\u5c71\u533a',
        u'\u95f5\u884c\u533a', u'\u5609\u5b9a\u533a', u'\u91d1\u5c71\u533a', u'\u677e\u6c5f\u533a',
        u'\u9752\u6d66\u533a', u'\u5d07\u660e', u'\u5949\u8d24\u533a', u'\u6b66\u6e05\u533a', u'\u5b81\u6cb3',
        u'\u5b9d\u577b\u533a', u'\u9759\u6d77', u'\u84df\u53bf', u'\u548c\u5e73\u533a', u'\u6cb3\u4e1c\u533a',
        u'\u6cb3\u897f\u533a', u'\u5357\u5f00\u533a', u'\u6cb3\u5317\u533a', u'\u7ea2\u6865\u533a',
        u'\u6ee8\u6d77\u65b0\u533a', u'\u4e1c\u4e3d\u533a', u'\u897f\u9752\u533a', u'\u5317\u8fb0\u533a',
        u'\u6d25\u5357\u533a', u'\u5949\u8282', u'\u6b66\u9686', u'\u5fe0\u53bf', u'\u5deb\u5c71',
        u'\u5f00\u53bf', u'\u6c38\u5ddd\u533a', u'\u8363\u660c', u'\u94dc\u6881', u'\u77f3\u67f1',
        u'\u5408\u5ddd\u533a', u'\u5357\u5ddd\u533a', u'\u957f\u5bff\u533a', u'\u5deb\u6eaa',
        u'\u9ed4\u6c5f\u533a', u'\u4e91\u9633', u'\u57ab\u6c5f', u'\u6881\u5e73', u'\u5927\u8db3\u533a',
        u'\u5317\u789a\u533a', u'\u74a7\u5c71', u'\u6c5f\u5317\u533a', u'\u6f7c\u5357', u'\u6daa\u9675\u533a',
        u'\u6c5f\u6d25\u533a', u'\u4e30\u90fd', u'\u57ce\u53e3', u'\u7da6\u6c5f\u533a', u'\u6e1d\u4e2d\u533a',
        u'\u5927\u6e21\u53e3\u533a', u'\u6c99\u576a\u575d\u533a', u'\u4e5d\u9f99\u5761\u533a',
        u'\u5357\u5cb8\u533a', u'\u6e1d\u5317\u533a', u'\u5df4\u5357\u533a', u'\u4e07\u5dde\u533a',
        u'\u79c0\u5c71', u'\u9149\u9633', u'\u5f6d\u6c34', u'\u5408\u80a5', u'\u6dee\u5357', u'\u868c\u57e0',
        u'\u5bbf\u5dde', u'\u961c\u9633', u'\u516d\u5b89', u'\u6ec1\u5dde', u'\u829c\u6e56', u'\u5b89\u5e86',
        u'\u9ec4\u5c71', u'\u94dc\u9675', u'\u6dee\u5317', u'\u4eb3\u5dde', u'\u9a6c\u978d\u5c71',
        u'\u6c60\u5dde', u'\u5ba3\u57ce', u'\u798f\u5dde', u'\u53a6\u95e8', u'\u6cc9\u5dde', u'\u5357\u5e73',
        u'\u6f33\u5dde', u'\u9f99\u5ca9', u'\u4e09\u660e', u'\u8386\u7530', u'\u5b81\u5fb7', u'\u5170\u5dde',
        u'\u5f20\u6396', u'\u6b66\u5a01', u'\u9152\u6cc9', u'\u91d1\u660c', u'\u5929\u6c34', u'\u5b9a\u897f',
        u'\u5e73\u51c9', u'\u7518\u5357', u'\u5609\u5cea\u5173', u'\u5e86\u9633', u'\u767d\u94f6',
        u'\u9647\u5357', u'\u4e34\u590f', u'\u5357\u5b81', u'\u67f3\u5dde', u'\u94a6\u5dde', u'\u767e\u8272',
        u'\u7389\u6797', u'\u9632\u57ce\u6e2f', u'\u6842\u6797', u'\u68a7\u5dde', u'\u6cb3\u6c60',
        u'\u5317\u6d77', u'\u8d35\u6e2f', u'\u6765\u5bbe', u'\u5d07\u5de6', u'\u8d3a\u5dde', u'\u8d35\u9633',
        u'\u516d\u76d8\u6c34', u'\u5b89\u987a', u'\u9075\u4e49', u'\u6bd5\u8282', u'\u94dc\u4ec1',
        u'\u9ed4\u897f\u5357', u'\u9ed4\u4e1c\u5357', u'\u9ed4\u5357', u'\u6d77\u53e3', u'\u4e09\u4e9a',
        u'\u7701\u76f4\u8f96\u53bf\u7ea7', u'\u77f3\u5bb6\u5e84', u'\u8861\u6c34', u'\u90a2\u53f0',
        u'\u90af\u90f8', u'\u6ca7\u5dde', u'\u5510\u5c71', u'\u5eca\u574a', u'\u79e6\u7687\u5c9b',
        u'\u627f\u5fb7', u'\u4fdd\u5b9a', u'\u5f20\u5bb6\u53e3', u'\u90d1\u5dde', u'\u65b0\u4e61',
        u'\u5b89\u9633', u'\u8bb8\u660c', u'\u9a7b\u9a6c\u5e97', u'\u6f2f\u6cb3', u'\u4fe1\u9633',
        u'\u5468\u53e3', u'\u6d1b\u9633', u'\u5e73\u9876\u5c71', u'\u4e09\u95e8\u5ce1', u'\u5357\u9633',
        u'\u5f00\u5c01', u'\u5546\u4e18', u'\u9e64\u58c1', u'\u6fee\u9633', u'\u7126\u4f5c',
        u'\u7701\u76f4\u8f96\u53bf\u7ea7', u'\u54c8\u5c14\u6ee8', u'\u7ee5\u5316', u'\u4f73\u6728\u65af',
        u'\u7261\u4e39\u6c5f', u'\u9f50\u9f50\u54c8\u5c14', u'\u5927\u5e86', u'\u5927\u5174\u5b89\u5cad',
        u'\u9e21\u897f', u'\u9e64\u5c97', u'\u53cc\u9e2d\u5c71', u'\u4f0a\u6625', u'\u9ed1\u6cb3',
        u'\u4e03\u53f0\u6cb3', u'\u6b66\u6c49', u'\u9ec4\u77f3', u'\u9102\u5dde', u'\u54b8\u5b81',
        u'\u5341\u5830', u'\u5b9c\u660c', u'\u6069\u65bd', u'\u8346\u5dde', u'\u9ec4\u5188', u'\u8346\u95e8',
        u'\u5b5d\u611f', u'\u8944\u9633', u'\u968f\u5dde', u'\u7701\u76f4\u8f96\u53bf\u7ea7', u'\u957f\u6c99',
        u'\u682a\u6d32', u'\u76ca\u9633', u'\u5cb3\u9633', u'\u5e38\u5fb7', u'\u5a04\u5e95', u'\u6000\u5316',
        u'\u8861\u9633', u'\u90b5\u9633', u'\u90f4\u5dde', u'\u5f20\u5bb6\u754c', u'\u6e58\u6f6d',
        u'\u6c38\u5dde', u'\u6e58\u897f', u'\u957f\u6625', u'\u5409\u6797', u'\u901a\u5316', u'\u56db\u5e73',
        u'\u767d\u57ce', u'\u677e\u539f', u'\u8fbd\u6e90', u'\u767d\u5c71', u'\u5ef6\u8fb9', u'\u5357\u4eac',
        u'\u82cf\u5dde', u'\u65e0\u9521', u'\u5f90\u5dde', u'\u5e38\u5dde', u'\u9547\u6c5f',
        u'\u8fde\u4e91\u6e2f', u'\u76d0\u57ce', u'\u626c\u5dde', u'\u5357\u901a', u'\u6dee\u5b89',
        u'\u6cf0\u5dde', u'\u5bbf\u8fc1', u'\u5357\u660c', u'\u4e5d\u6c5f', u'\u666f\u5fb7\u9547',
        u'\u4e0a\u9976', u'\u9e70\u6f6d', u'\u5b9c\u6625', u'\u840d\u4e61', u'\u8d63\u5dde', u'\u5409\u5b89',
        u'\u629a\u5dde', u'\u65b0\u4f59', u'\u6c88\u9633', u'\u94c1\u5cad', u'\u629a\u987a', u'\u978d\u5c71',
        u'\u8425\u53e3', u'\u5927\u8fde', u'\u672c\u6eaa', u'\u4e39\u4e1c', u'\u9526\u5dde', u'\u671d\u9633',
        u'\u961c\u65b0', u'\u76d8\u9526', u'\u8fbd\u9633', u'\u846b\u82a6\u5c9b', u'\u547c\u548c\u6d69\u7279',
        u'\u5305\u5934', u'\u4e4c\u6d77', u'\u8d64\u5cf0', u'\u901a\u8fbd', u'\u9521\u6797\u90ed\u52d2\u76df',
        u'\u963f\u62c9\u5584\u76df', u'\u5174\u5b89\u76df', u'\u9102\u5c14\u591a\u65af',
        u'\u547c\u4f26\u8d1d\u5c14', u'\u5df4\u5f66\u6dd6\u5c14', u'\u4e4c\u5170\u5bdf\u5e03', u'\u94f6\u5ddd',
        u'\u77f3\u5634\u5c71', u'\u56fa\u539f', u'\u5434\u5fe0', u'\u4e2d\u536b', u'\u897f\u5b81',
        u'\u679c\u6d1b', u'\u7389\u6811', u'\u6d77\u897f', u'\u6d77\u4e1c', u'\u6d77\u5317', u'\u9ec4\u5357',
        u'\u6d77\u5357', u'\u9752\u5c9b', u'\u5a01\u6d77', u'\u6d4e\u5357', u'\u6dc4\u535a', u'\u804a\u57ce',
        u'\u5fb7\u5dde', u'\u4e1c\u8425', u'\u6f4d\u574a', u'\u70df\u53f0', u'\u6cf0\u5b89', u'\u83cf\u6cfd',
        u'\u4e34\u6c82', u'\u67a3\u5e84', u'\u6d4e\u5b81', u'\u65e5\u7167', u'\u6ee8\u5dde', u'\u83b1\u829c',
        u'\u592a\u539f', u'\u5ffb\u5dde', u'\u5927\u540c', u'\u4e34\u6c7e', u'\u8fd0\u57ce', u'\u9633\u6cc9',
        u'\u957f\u6cbb', u'\u664b\u57ce', u'\u6714\u5dde', u'\u664b\u4e2d', u'\u5415\u6881', u'\u897f\u5b89',
        u'\u6e2d\u5357', u'\u5ef6\u5b89', u'\u6986\u6797', u'\u5b9d\u9e21', u'\u5b89\u5eb7', u'\u6c49\u4e2d',
        u'\u94dc\u5ddd', u'\u54b8\u9633', u'\u5546\u6d1b', u'\u6210\u90fd', u'\u4e50\u5c71', u'\u51c9\u5c71',
        u'\u7ef5\u9633', u'\u963f\u575d', u'\u96c5\u5b89', u'\u7518\u5b5c', u'\u5e7f\u5143', u'\u5357\u5145',
        u'\u5185\u6c5f', u'\u81ea\u8d21', u'\u5b9c\u5bbe', u'\u6cf8\u5dde', u'\u6500\u679d\u82b1',
        u'\u5fb7\u9633', u'\u8d44\u9633', u'\u7709\u5c71', u'\u5e7f\u5b89', u'\u9042\u5b81', u'\u5df4\u4e2d',
        u'\u8fbe\u5dde', u'\u62c9\u8428', u'\u90a3\u66f2', u'\u660c\u90fd', u'\u5c71\u5357',
        u'\u65e5\u5580\u5219', u'\u963f\u91cc', u'\u6797\u829d', u'\u4e4c\u9c81\u6728\u9f50',
        u'\u514b\u62c9\u739b\u4f9d', u'\u963f\u52d2\u6cf0', u'\u5df4\u97f3\u90ed\u695e', u'\u54c8\u5bc6',
        u'\u5410\u9c81\u756a', u'\u963f\u514b\u82cf', u'\u5580\u4ec0', u'\u548c\u7530', u'\u660c\u5409',
        u'\u5854\u57ce', u'\u514b\u5b5c\u52d2\u82cf', u'\u535a\u5c14\u5854\u62c9', u'\u4f0a\u7281',
        u'\u81ea\u6cbb\u533a\u76f4\u8f96\u53bf\u7ea7', u'\u6606\u660e', u'\u66f2\u9756', u'\u662d\u901a',
        u'\u6587\u5c71', u'\u5927\u7406', u'\u695a\u96c4', u'\u4e34\u6ca7', u'\u4fdd\u5c71', u'\u7389\u6eaa',
        u'\u4e3d\u6c5f', u'\u666e\u6d31', u'\u7ea2\u6cb3\u5dde', u'\u897f\u53cc\u7248\u7eb3', u'\u5fb7\u5b8f',
        u'\u6012\u6c5f', u'\u8fea\u5e86', u'\u676d\u5dde', u'\u6e29\u5dde', u'\u5b81\u6ce2', u'\u7ecd\u5174',
        u'\u6e56\u5dde', u'\u5609\u5174', u'\u91d1\u534e', u'\u4e3d\u6c34', u'\u8862\u5dde', u'\u53f0\u5dde',
        u'\u821f\u5c71', u'\u6fb3\u95e8', u'\u9999\u6e2f\u5c9b', u'\u4e5d\u9f99', u'\u65b0\u754c',
        u'\u4e91\u6797', u'\u65b0\u5317', u'\u53f0\u5317', u'\u9ad8\u96c4', u'\u6843\u56ed', u'\u65b0\u7af9',
        u'\u5b9c\u5170', u'\u82d7\u6817', u'\u5c4f\u4e1c', u'\u82b1\u83b2', u'\u5f70\u5316', u'\u5357\u6295',
        u'\u53f0\u4e1c', u'\u57fa\u9686', u'\u53f0\u4e2d', u'\u53f0\u5357', u'\u5609\u4e49', u'\u6f8e\u6e56']

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
    contacts = Contact.query.order_by(Contact.name).all()
    data = list()

    for item in contacts:
        tmp = dict()
        tmp['account'] = item.name
        tmp_ip = list()
        for i in range(0, 4):
            tmp_ip.append(str(random.randint(0,255)))
        tmp_ip_string = '.'.join(tmp_ip)
        tmp['ip'] = tmp_ip_string
        tmp_city_id = random.randint(1, len(all_city) + 1)
        tmp['location'] = all_city[tmp_city_id]
        tmp_isp_id = random.randint(1, 4)
        if tmp_isp_id == 1:
            tmp['isp'] = '中国电信'
        if tmp_isp_id == 2:
            tmp['isp'] = '中国联通'
        if tmp_isp_id == 3:
            tmp['isp'] = '其他'
        data.append(tmp)

    return render_template('web/test1.html', contacts=data)

@app.route("/test2", methods=('GET', 'POST'))
@login_required
def test2():

    contacts = Contact.query.order_by(Contact.name).all()
    data = list()

    for item in contacts:
        tmp = dict()
        tmp['account'] = item.name

        tmp_time = list()
        tmp_time.append(str(random.randint(0,24)))
        tmp_time.append(str(random.randint(0,60)))
        tmp_time.append(str(random.randint(0,60)))
        tmp_time_string = ':'.join(tmp_time)
        tmp['login'] = tmp_time_string

        base = random.randint(1, 30)
        tmp['duration'] = str(base)
        tmp['total'] = str(base + random.randint(1, 100))

        data.append(tmp)

    return render_template('web/test2.html', contacts=data)

@app.route("/test3", methods=('GET', 'POST'))
@login_required
def test3():

    contacts = Contact.query.order_by(Contact.name).all()
    data = list()

    for item in contacts:
        tmp = dict()
        tmp['account'] = item.name
        base = random.randint(1, 10)
        tmp['count'] = str(base)

        data.append(tmp)

    return render_template('web/test3.html', contacts=data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
