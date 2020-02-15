from . import db

class Worker(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(30))
    lname = db.Column(db.String(30))
    address1 = db.Column(db.String(100))
    city = db.Column(db.String(30))
    country = db.Column(db.String(30))
    telephone = db.Column(db.String(20))
    role = db.Column(db.String(100))
    email = db.Column(db.String(50))

    def __init__(self, fname, lname, address1, city, country, telephone, role, email):
        self.fname = fname
        self.lname = lname
        self.address1 = address1
        self.city = city
        self.country = country
        self.telephone = telephone
        self.role = role
        self.email = email

    def __repr__(self):
        return '%r, %r, %r, %r, %r, %r, %r, %r' % self.fname, self.lname, self.address1, self.city, self.country, self.telephone, self.role, self.email
