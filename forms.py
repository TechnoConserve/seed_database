from flask_wtf import FlaskForm
from wtforms import DateField, FloatField, SelectField, StringField
from wtforms.validators import (DataRequired, ValidationError)

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


class ShipmentForm(FlaskForm):
    ship_date = DateField(
        'Shipment Date',
        validators=[DataRequired()],
        format='%m-%d-%Y')
    tracking_num = StringField(
        'Tracking Number',
        validators=[
            DataRequired(),
            shipment_exists
        ])
    tracking_num_comp = SelectField(
        'Company',
        validators=[DataRequired()],
        choices=COMPANIES)
    amount_gr = FloatField(
        'Amount in grams',
        validators=[DataRequired()])
    calc_by = SelectField(
        'Amount calculated by...',
        validators=[DataRequired()],
        choices=[('ct', 'Counting'), ('wt', 'Weighed')])
    origin_institute_id = SelectField('Origin', coerce=int)
    destination_institute_id = SelectField('Destination', coerce=int)
    accession = SelectField('Accession', coerce=int)


class SpeciesForm(FlaskForm):
    symbol = StringField(
        'Symbol',
        validators=[DataRequired()]
    )
    name_full = StringField(
        'Full name',
        validators=[DataRequired()]
    )
    common = StringField(
        'Common name',
        validators=[DataRequired()]
    )
    family = StringField(
        'Family',
        validators=[DataRequired()]
    )
    genus = StringField(
        'Genus',
        validators=[DataRequired()]
    )
    species = StringField(
        'Species',
        validators=[DataRequired()]
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
