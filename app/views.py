from app import app
from flask import render_template, request, redirect, url_for, flash
from app.models import Worker
from . import db
from .forms import WorkerF
from app import mail
from flask_mail import Message


@app.route('/')
def home():
    """Render website's home page."""
    #db.create_all()
    return render_template('home.html')

@app.route('/addworker', methods=['GET', 'POST'])
def addWorker():
    workerF = WorkerF()
    if request.method == 'POST':
        if workerF.validate_on_submit():
            fname = workerF.fname.data
            lname = workerF.lname.data
            address1 = workerF.address1.data
            city = workerF.city.data
            country = workerF.country.data
            telephone = workerF.telephone.data
            role = workerF.role.data
            email = workerF.email.data

            worker = Worker(fname, lname, address1, city, country, telephone, role, email)
            db.session.add(worker)
            db.session.commit()
            
            flash('Worker successfully added!', 'success')
            return redirect(url_for('home'))

        flash_errors(worker)
    return render_template('addworker.html', form=workerF)

###
# The functions below should be applicable to all Flask apps.
###

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
