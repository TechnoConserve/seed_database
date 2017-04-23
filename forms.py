from flask_wtf import FlaskForm
from wtforms import DateField, FloatField, IntegerField, SelectField, StringField, TextAreaField
from wtforms import validators

from models import Shipping

COMPANIES = [('FedEx', 'FedEx'), ('UPS', 'UPS'), ('USPS', 'USPS')]
DURATION_CHOICES = [('Annual', 'Annual'), ('Perennial', 'Perennial'), ('Biennial', 'Biennial'), ('Monocarpic', 'Monocarpic')]
TYPE_CHOICES = [
    ('Graminoid', 'Graminoid'),
    ('Forb/Herb', 'Forb/Herb'),
    ('Tree', 'Tree'),
    ('Shrub', 'Shrub'),
    ('Subshrub', 'Subshrub'),
    ('Vine', 'Vine'),
]


def shipment_exists(field):
    if Shipping.select().where(Shipping.tracking_num == field.data).exists():
        raise validators.ValidationError('Shipment with that tracking number already exists.')


class AccessionForm(FlaskForm):
    family = SelectField(
        'Family'
    )
    genus = SelectField(
        'Genus'
    )
    species = SelectField(
        'Species',
        coerce=int
    )
    data_source = StringField(
        'Data Source',
        validators=[validators.length(max=30)]
    )
    plant_habit = SelectField(
        'Plant Habit',
        choices=TYPE_CHOICES,
        validators=[validators.length(max=30)]
    )
    coll_date = DateField(
        'Collection Date',
        validators=[validators.InputRequired()]
    )
    acc_num = StringField(
        'Accession Number',
        validators=[validators.InputRequired(), validators.length(max=10)]
    )
    collected_with = StringField(
        'Collectors',
        validators=[validators.InputRequired(), validators.length(max=100)]
    )
    collection_misc = TextAreaField(
        'Collection Miscellaneous',
    )
    seed_source = StringField(
        'Seed Source',
        validators=[validators.length(max=100)]
    )
    description = TextAreaField(
        'Description',
    )
    notes = TextAreaField(
        'Notes'
    )
    # Location Fields
    phytoregion = StringField(
        'Phytoregion Code',
        validators=[validators.length(max=30)]
    )
    phytoregion_full = StringField(
        'Phytoregion Full',
        validators=[validators.length(max=50)]
    )
    locality = StringField(
        'Locality',
        validators=[validators.length(max=50)]
    )
    geog_area = StringField(
        'Geographic Area',
        validators=[validators.length(max=50)]
    )
    directions = TextAreaField(
        'Directions',
    )
    degrees_n = IntegerField(
        'Degrees North'
    )
    minutes_n = IntegerField(
        'Minutes North'
    )
    seconds_n = IntegerField(
        'Seconds North'
    )
    degrees_w = IntegerField(
        'Degrees West'
    )
    minutes_w = IntegerField(
        'Minutes West'
    )
    seconds_w = IntegerField(
        'Seconds West'
    )
    latitute_decimal = FloatField(
        'Latitude Decimal'
    )
    longitude_decimal = FloatField(
        'Longitude Decimal'
    )
    georef_source = StringField(
        'Source of Geographic Information',
        validators=[validators.length(max=50)]
    )
    gps_datum = StringField(
        'Datum',
        validators=[validators.length(max=10)]
    )
    altitude = IntegerField(
        'Altitude'
    )
    altitude_unit = SelectField(
        'Unit',
        choices=[('ft', 'Feet'), ('m', 'Meters')]
    )
    fo_name = StringField(
        'Field Office Name',
        validators=[validators.length(max=50)]
    )
    district_name = StringField(
        'District Name',
        validators=[validators.length(max=50)]
    )
    state = StringField(
        'State',
        validators=[validators.length(max=20)]
    )
    county = StringField(
        'County',
        validators=[validators.length(max=30)]
    )
    # Location Description Fields
    land_owner = StringField(
        'Land Owner',
        validators=[validators.length(max=30)]
    )
    associated_taxa_full = TextAreaField(
        'Associated Taxa'
    )
    mod = StringField(
        'Modifying factors',
        validators=[validators.length(max=200)]
    )
    mod2 = StringField(
        'Additional Modifying Factors',
        validators=[validators.length(max=200)]
    )
    geomorphology = StringField(
        'Geomorphology',
        validators=[validators.length(max=100)]
    )
    slope = StringField(
        'Slope',
        validators=[validators.length(max=30)]
    )
    aspect = StringField(
        'Aspect',
        validators=[validators.length(max=10)]
    )
    habitat = StringField(
        'Habitat',
        validators=[validators.length(max=100)]
    )
    geology = StringField(
        'Geology',
        validators=[validators.length(max=100)]
    )
    soil_type = StringField(
        'Soil Type',
        validators=[validators.length(max=100)]
    )
    population_size = IntegerField(
        'Population Size'
    )
    occupancy = IntegerField(
        'Occupancy'
    )


class InstitutionForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[validators.InputRequired()]
    )
    address = StringField(
        'Address',
        validators=[validators.InputRequired()]
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
        validators=[validators.Email()]
    )
    request_costs = StringField(
        'Request Costs?'
    )


class ShipmentForm(FlaskForm):
    ship_date = DateField(
        'Shipment Date',
        validators=[validators.InputRequired()],
        format='%m-%d-%Y')
    tracking_num = StringField(
        'Tracking Number',
        validators=[
            validators.InputRequired(),
            shipment_exists
        ])
    tracking_num_comp = SelectField(
        'Company',
        validators=[validators.InputRequired()],
        choices=COMPANIES)
    amount_gr = FloatField(
        'Amount in grams',
        validators=[validators.InputRequired()])
    calc_by = SelectField(
        'Amount calculated by...',
        validators=[validators.InputRequired()],
        choices=[('ct', 'Counting'), ('wt', 'Weighed')])
    origin_institute_id = SelectField('Origin', coerce=int)
    destination_institute_id = SelectField('Destination', coerce=int)
    accession = SelectField('Accession', coerce=int)


class SpeciesForm(FlaskForm):
    symbol = StringField(
        'Symbol',
        validators=[validators.InputRequired()]
    )
    name_full = StringField(
        'Full name',
        validators=[validators.InputRequired()]
    )
    common = StringField(
        'Common name',
        validators=[validators.InputRequired()]
    )
    family = StringField(
        'Family',
        validators=[validators.InputRequired()]
    )
    genus = StringField(
        'Genus',
        validators=[validators.InputRequired()]
    )
    species = StringField(
        'Species',
        validators=[validators.InputRequired()]
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


class SynonymsForm(FlaskForm):
    species = SelectField(
        'Species',
        validators=[validators.input_required()],
        coerce=int,
    )
    synonym = SelectField(
        'Synonym',
        validators=[validators.input_required()],
        coerce=int,
    )
