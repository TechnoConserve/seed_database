**Creating a table**

This document describes the process of creating a new table in the
[MySQL database](https://dev.mysql.com/doc/refman/5.7/en/). Tables are
defined as [Python](https://docs.python.org/3.5/tutorial/index.html)
classes which extend a
[SQLAlchemy](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#create-a-schema)
model. SQLAlchemy translates the Python model into a raw SQL query which
creates the MySQL table. Since the database is being designed for use
with a web interface, the code makes use of
[Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.1/quickstart/), a
library that, as its name suggests, integrates SQLAlchemy with Flask.
[Flask](http://flask.pocoo.org/docs/0.12/) is the library that deals
with the web component, allowing for a web interface to control the
underlying database.

**Defining the table**

We will be making a new table called Contact which will hold information
about people related to a particular institution. Conventionally, tables
are named with the singular form of the data they contain which is why
we are naming it Contact, and not Contacts. You begin defining the table
by defining the name of the Python class:

```python
class Contact(db.Model):
```

Here we have defined a class named Contact which derives from another
class in SQLAlchemy that we have referenced by including the db.Model in
the parentheses. Luckily we don’t need to understand much about what
db.Model does or how it works. SQLAlchemy handles that for us! By
creating a class this way we’re just telling SQLAlchemy that we are
defining a model that we would like translated into a database table.

**Everything below this line must now be indented to be included in the
Contact table.** You should strive to use 4 spaces as the indentation
level but Python doesn’t care so long as you stay consistent. It’s
important to use the same indentation level as is used in the rest of
the file or the code won’t be able to run. Python uses whitespace to
figure out how code is related. Thus, everything we indent after
defining our Contact class, Python will know to interpret as being a
part of that class.

Immediately below this line (indented!), it’s a good idea to include
what is called a docstring. It is simply a description of the code you
are writing. It is not evaluated when the code is executed so you can
type whatever you want. You begin a docstring using three quotes (“””)
and end the docstring the same way. Between your pair of three quote
marks, you can describe in plain English what the table is for, and how
it relates to other tables. The purpose of a docstring is to help you
and or other people reading your code understand what is going on and
what you are trying to achieve.

The docstring I created for the Contact table looks like this:
```python
    """
    The Contacts table has a Many-to-One relationship with the
    Institution table.
    
    The Contacts table has a Many-to-One relationship with the
    Address table.
    
    A contact represents a person of significance related to a
    particular institution. As an example, for each seed storage 
    institution, the person responsible for managing seed shipments out 
    of that institution should be added as a Contact record.
    """
```

After the docstring, on a new line, we define the name of our table:
```python
    __tablename__ = 'contact'
```

This defines a special variable “\_\_tablename\_\_” as a string value
named “contact” (note that tablename is surrounded on both sides by two
underscores). A string value in Python is just normal text. It is
denoted by the quote marks. Either single or double quote marks can be
used to define a string, it’s up to you.[1] Whichever one you decide,
it’s best to stay consistent.

Because of the Python libraries we are using, defining a tablename in
this way isn’t strictly necessary. If we don’t define it, the name of
the table will default to the name of the class, which we named Contact.
So in this particular case, it would be exactly the same even if we
removed our tablename definition. I’ve chosen to include it regardless
because it makes the code more readable (in my opinion).

**Defining the fields**

At this point we define the table fields. Each table field represents a
column in the resulting database table. The order in which we define the
fields will determine the order in which the columns appear in the
database table so it makes sense to define them in a logical order.

The first field to define is the primary key. The primary key is
critical to the proper functioning of a relational database as it allows
a particular record to be referenced by other objects that can exist in
the same or other tables (or even other databases). Conventionally we
name the primary key ‘id’ and define it like so:
```python
    id = db.Column(db.Integer, primary_key=True)
```

At this point, we have told the database to create a table called
contact that has a single column named id. In our id declaration we have
included two important parameters as well. The first, “db.Integer”,
tells the database that this column will contain Integer values. The
database will be unable to hold any other type of data in this column.
Attempting to do so would produce an error. A full list of possible
Column types can be found in the [SQLAlchemy
documentation](http://docs.sqlalchemy.org/en/latest/core/type_basics.html?highlight=column%20types).
Keep in mind, we are using Flask-SQLAlchemy to control the database
definitions, so the code examples found in the SQLAlchemy documentation
may need to be tweaked before they will work with our database
connection.

The second parameter, “primary\_key”, is assigned the value of True by
using the “=” sign, which tells the database that the id field will be
used as the primary key for this table. When we create our first Contact
record, the object will be automatically assigned a unique id value, so
we don’t have to worry about doing it ourselves. We can then refer back
to this id value and know exactly which record we are talking about.

Now we can worry about what sort of information we want the contact
table to contain. In this case we want things like first name, last
name, email address, telephone number (and extension), title, and
agency.

We’ll start with a field for a first name:
```python
    first_name = db.Column(db.String(30))
```

Here we are creating a field called “first\_name” that we define as a
database Column as we did previously. In this case though we only have a
single parameter “db.String”, which itself has its own parameter which
we have given as “30”.

“db.String”, just like “db.Integer” from the “id” field we defined
before, determines the datatype of the field. We expect a person’s first
name to be a text (aka string) value, so we have defined this Column to
contain string values. The string datatype definition differs further
from the integer datatype in that it requires us to specify a maximum
character length for the data that the column will store. I have chosen,
somewhat arbitrarily, “30” because I do not anticipate needing the
database to store a first name that exceeds 30 characters in length.

There are some tradeoffs to consider when deciding how long a field
should be. It is best to err on the side of generosity, otherwise you
risk creating errors when users try to enter legitimate data that has a
longer character length than what the database expects. That said, you
should also strive to define fields with the minimum amount of space
required for the job. This keeps the size of the database small since
the database needs to allocate less space to store those fields. Also,
defining the minimal amount of space can help your users correct
mistakes when inputting new data. For example, if a user accidently
pasted in a sentence to the “first\_name” field, the database would
throw an error because it is expecting no more than 30 characters in
that field. If instead we had allowed 300 characters in that field, the
database would not have complained and the user may not have noticed
their error at all when saving the data.

Lastly, it’s worth pointing out that we can call our variable whatever
we want. We could have called “first\_name” just “f” or “f\_n”.
Obviously though, it’s in our best interest to give our variables clear
and descriptive names so it is immediately obvious what sort of
information they are meant to contain.

Now we can add the remaining descriptive fields to the table model:
```python
    last_name = db.Column(db.String(40))
    email = db.Column(db.String(50))
    telephone = db.Column(db.Integer)
    tel_ext = db.Column(db.Integer)  # Telephone extension
    title = db.Column(db.String(50))  # Job title
    agency = db.Column(db.String(50))  # Who do they work for?
```

The only thing here we haven’t seen before are the inline comments
beside the “tel\_ext”, “title”, and “agency” fields. These comments are
meant for human readers, not the computer, and can be used to provide a
brief explanation of what the code is doing. You can add these anywhere
in the code using the pound symbol (“\#”). Anything to the right of the
pound sign will be ignored when the code is interpreted. If you need to
write a longer comment that will span multiple lines, you can use the
pair of three quote marks just as we did with the docstring above. In
this case, everything between the pair of triple quotes will be ignored
by the interpreter.

**Establishing**
[**Relationships**](http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html)

At this point, our Contact table is nearly done but it isn’t very useful
until we link it to other tables with a database relationship. Each
contact should have an address and be related to an institution so we
should create relationships to those two tables.

**Many-to-One**

For both the Address and Institution table, the relationship will be
Many-to-One from the Contact table. In other words, there can be
multiple contacts related to a single address and a single institution.

The link between the tables is maintained by what is called a
ForeignKey. We will give the Contact table one column for each
ForeignKey we need it to hold, one for the Address table and one for the
Institution table. Each ForeignKey column holds an integer value that
corresponds to one of the unique primary key values of the outside, or
“foreign”, table. This will establish Many-to-One relationships between
the Contact table and the Address and Institution tables.

We start to link the tables like so:
```python
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    institution_id = db.Column(db.Integer, db.ForeignKey('institution.id'))
```

The “db.ForeignKey” parameter again requires a parameter of its own. In
this case, it asks for the primary key field of the table you would like
to link to. For the “address\_id” field we want to link to the Address
table which we have given the “\_\_tablename\_\_” as “address”. We need
to reference the “primary\_key” field, which by convention, I’ve named
“id”. We do this by typing in quotes the tablename and the name of the
field, separated by a period. Hence: “‘address.id’”.

For reference, I’ve included the code of the Address table below:
```python
class Address(db.Model):
    """
    The Address table has a One-to-Many relationship with the
    Contacts and the Institution tables.
    """
    __tablename__ = 'address'

    id = db.Column(db.Integer, primary_key=True)
    address_one = db.Column(db.String(100))
    address_two = db.Column(db.String(100))
    state = db.Column(db.String(20))
    city = db.Column(db.String(25))
    zipcode = db.Column(db.Integer)
```

At the bottom of this model we need to add the relationship back to
contacts:
```python
    contacts = db.relationship('Contact', backref='address')
```

For this relationships we’re using the function “db.relationship” and
passing in two parameters. The first one is the name of the class for
the table we want to link to. The “backref” parameter is especially
important because it establishes a relationship in reverse, or in other
words, a back reference, hence the name of the parameter. So in this
case, we’re establishing a relationship from the Address table while
essentially establishing an additional field in the Contact table using
the “backref” parameter. Given this parameter, any instance of the
Contact table will now have an attribute called “address” that will
return the address associated with that Contact.

Now to create the relationship between the Contact and Institution
table. Add the following to the Institution table:
```python
    contacts = db.relationship('Contact', backref='institute')
```

Since it’s the same type of relationship, the code is very similar. The
only difference is now we give the “backref” parameter the string value
“’institute’” so that instances of the Contact table will can have an
“institute” attribute. Just like the “address” attribute we added,
accessing a Contact’s “institute” attribute would return the Institution
object (AKA table row) that it is related to.

**Many-to-Many**

Each Contact might also be associated with multiple Projects. And each
Project could be associated with multiple Contacts. This sort of
relationship is called a Many-to-Many relationship and it necessitates
what’s called a helper, or association, table. The helper table stores
nothing except the foreign keys of the tables it is helping to relate,
so it doesn’t need to be a derivative of the “db.Model” class like the
other tables we’ve seen.

We can write a helper table like this:
```python
project_contacts = db.Table('project_contacts',
                            db.Column('project_id', db.Integer, db.ForeignKey('project.id')),
                            db.Column('contact_id', db.Integer, db.ForeignKey('contact.id'))
                            )
```

Now we can jump back to our Contact table to finish the relationship.
Add the following to the bottom of the Contact table model:
```python
    projects = db.relationship('Project', secondary=project_contacts,
                               backref=db.backref('contacts', lazy='dynamic'))
```

This relationship is just a bit more complicated than the last ones.
Like before, the first parameter is the name of the class we are linking
to, which is the Project table. The next parameter, “secondary”, is
unique to Many-to-Many relationships and it requires the name of the
helper table which we named “project\_contacts”. The “backref” parameter
is also a little different this time. We could have simply passed this
parameter the string “’contacts’” and it would have worked. Instead,
we’re passing it another function, “db.backref”, which allows gives use
some additional functionality. The “db.backref” function takes two
parameters of its own, the first being “’contacts’” which works the same
way we’ve seen before. This gives instances of the Project table the
additional attribute “contacts” so each project can be queried for the
contacts related to that project. The second parameter of “db.backref”,
“lazy”, describes what [type of
query](http://flask-sqlalchemy.pocoo.org/2.1/models/) is returned when
projects are queried for their related contacts.

From the Flask-SQLAlchemy docs, we see that passing ‘dynamic’ to the
“lazy” parameter means the following:

-   'dynamic' is special and useful if you have many items. Instead of
    > loading the items SQLAlchemy will return another query object
    > which you can further refine before loading the items. This is
    > usually what you want if you expect more than a handful of items
    > for this relationship.

You’ve now successfully created a Contact table with two Many-to-One
relationships and one Many-to-Many relationship! For reference, here is
all the code we just typed in one place:
```python
class Contact(db.Model):
    """
    The Contacts table has a Many-to-One relationship with the
    Institution table.
    
    The Contacts table has a Many-to-One relationship with the
    Address table.
    
    A contact represents a person of significance related to a
    particular institution. As an example, for each seed storage 
    institution, the person responsible for managing seed shipments out 
    of that institution should be added as a Contact record.
    """
    __tablename__ = 'contact'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(40))
    email = db.Column(db.String(50))
    telephone = db.Column(db.Integer)
    tel_ext = db.Column(db.Integer)  # Telephone extension
    title = db.Column(db.String(50))  # Job title
    agency = db.Column(db.String(50))  # Who do they work for?

    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    institution_id = db.Column(db.Integer, db.ForeignKey('institution.id'))

    projects = db.relationship('Project', secondary=project_contacts,
                               backref=db.backref('contacts', lazy='dynamic'))
```

[1] If you want to learn more about stylistic guidelines in Python, you
should check out the [PEP 8
guidelines](https://www.python.org/dev/peps/pep-0008/). Following these
guidelines will make your code easier to read, which in turn makes it
easier to maintain, especially for others.