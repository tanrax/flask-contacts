from flask import Flask, redirect, url_for, render_template, request, flash
from models import db, Contact
from forms import ContactForm

# Flask
app = Flask(__name__)
app.secret_key = 'my secret'

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/book'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.context_processor
def add_lang_to_templates():
    return {'lang': 'en'}

db.init_app(app)


@app.route("/")
def index():
    '''
    Home page
    '''
    return redirect(url_for('contacts'))


@app.route("/new_contact", methods=('GET', 'POST'))
def new_contact():
    '''
    Create new contact
    '''
    form = ContactForm()
    if form.validate_on_submit():
        # Get form
        name = form.name.data
        surname = form.surname.data
        email = form.email.data
        phone = form.phone.data
        # Save in database
        try:
            my_contact = Contact(name, surname, email, phone)
            db.session.add(my_contact)
            db.session.commit()
            # User info
            flash('Contact created correctly', 'success')
            return redirect(url_for('contacts'))
        except:
            db.session.rollback()
            flash('Error generating contact.', 'danger')

    return render_template('web/new_contact.html', form=form)


@app.route("/edit_contact/<id>", methods=('GET', 'POST'))
def edit_contact(id):
    '''
    Edit contact

    :param id: Id from contact
    '''    
    rtn = None
    my_contact = Contact.query.filter_by(id=id).first()
    if request.method.lower() == 'get':
        form = ContactForm(obj=my_contact)
    else:
        form = ContactForm()
        if form.validate_on_submit():
            form.populate_obj(my_contact)
            # Get form
            name = form.name.data
            surname = form.surname.data
            email = form.email.data
            phone = form.phone.data
            try:
                # Update contact
                my_contact.name = name
                my_contact.surname = surname
                my_contact.email = email
                my_contact.phone = phone
                db.session.add(my_contact)
                db.session.commit()
                # User info
                flash('Saved successfully', 'success')
                rtn = redirect(url_for('index'))
            except:
                db.session.rollback()
                flash('Error updating contact.', 'danger')    
    return rtn if rtn is not None else render_template(
        'web/edit_contact.html',
        form=form,
        contact_id=my_contact.id)


@app.route("/contacts")
def contacts():
    '''
    Show alls contacts
    '''
    contacts = Contact.query.order_by(Contact.name).all()
    return render_template('web/contacts.html', contacts=contacts)


@app.route("/search")
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
def contacts_delete():
    '''
    Delete contact

    :param id: Id from contact
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
    app.debug = True
    app.run(host='0.0.0.0', port=8888, debug=True)
