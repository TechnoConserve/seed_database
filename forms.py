from flask_wtf import Form
from wtforms import DateField, FloatField, IntegerField, SelectField, StringField
from wtforms.validators import (Email, InputRequired, ValidationError)

from models import Shipping

COMPANIES = [('fx', 'FedEx'), ('ups', 'UPS'), ('usps', 'USPS')]
DURATION_CHOICES = [('ann', 'Annual'), ('per', 'Perennial'), ('bi', 'Biennial'), ('mon', 'Monocarpic')]
TYPE_CHOICES = [
    ('gram', 'Graminoid'),
    ('forb', 'Forb/Herb'),
    ('tree', 'Tree'),
    ('shrub', 'Shrub'),
    ('sub', 'Subshrub'),
    ('vine', 'Vine'),
]


def shipment_exists(field):
    if Shipping.select().where(Shipping.tracking_num == field.data).exists():
        raise ValidationError('Shipment with that tracking number already exists.')


class InstitutionForm(Form):
    name = StringField(
        'Name',
        validators=[InputRequired()]
    )
    address = StringField(
        'Address',
        validators=[InputRequired()]
    )
    contact_name = StringField(
        'Contact Name'
    )
    contact_phone = IntegerField(
        'Contact Phone'
    )
    contact_phone_ext = IntegerField(
        'Contact Phone Extension'
    )
    contact_email = StringField(
        'Contact Email',
        validators=[Email()]
    )
    request_costs = StringField(
        'Request Costs?'
    )


class ShipmentForm(Form):
    ship_date = DateField(
        'Shipment Date',
        validators=[InputRequired()],
        format='%m-%d-%Y')
    tracking_num = StringField(
        'Tracking Number',
        validators=[
            InputRequired(),
            shipment_exists
        ])
    tracking_num_comp = SelectField(
        'Company',
        validators=[InputRequired()],
        choices=COMPANIES)
    amount_gr = FloatField(
        'Amount in grams',
        validators=[InputRequired()])
    calc_by = SelectField(
        'Amount calculated by...',
        validators=[InputRequired()],
        choices=[('ct', 'Counting'), ('wt', 'Weighed')])
    origin_institute_id = SelectField('Origin', coerce=int)
    destination_institute_id = SelectField('Destination', coerce=int)
    accession = SelectField('Accession', coerce=int)


class SpeciesForm(Form):
    symbol = StringField(
        'Symbol',
        validators=[InputRequired()]
    )
    name_full = StringField(
        'Full name',
        validators=[InputRequired()]
    )
    common = StringField(
        'Common name',
        validators=[InputRequired()]
    )
    family = StringField(
        'Family',
        validators=[InputRequired()]
    )
    genus = StringField(
        'Genus',
        validators=[InputRequired()]
    )
    species = StringField(
        'Species',
        validators=[InputRequired()]
    )
    var_ssp1 = SelectField(
        'ssp / var',
        choices=[('ssp', 'ssp'), ('var', 'var')]
    )
    var_ssp2 = StringField(
        'ssp / var name',
    )
    plant_type = SelectField(
        'Type',
        choices=TYPE_CHOICES
    )
    plant_duration = SelectField(
        'Duration',
        choices=DURATION_CHOICES
    )
