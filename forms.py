from flask_wtf import FlaskForm
from wtforms import BooleanField, DateField, FloatField, IntegerField, SelectField, StringField, TextAreaField
from wtforms import validators

from models import Shipment

COMPANIES = [('FedEx', 'FedEx'), ('UPS', 'UPS'), ('USPS', 'USPS')]
DURATION_CHOICES = [
    ('Annual', 'Annual'), ('Perennial', 'Perennial'), ('Biennial', 'Biennial'), ('Monocarpic', 'Monocarpic')]
TYPE_CHOICES = [
    ('Graminoid', 'Graminoid'),
    ('Forb/Herb', 'Forb/Herb'),
    ('Tree', 'Tree'),
    ('Shrub', 'Shrub'),
    ('Subshrub', 'Subshrub'),
    ('Vine', 'Vine'),
]
PHYTOREGION_CODES = [
    ('11E', 'Blue Mountains (Omernik)'),
    ('12E', 'Snake River Plain (Omernik)'),
    ('13E', 'Central Basin and Range (Omernik)'),
    ('14E', 'Mojave Basin and Range (Omernik)'),
    ('18E', 'Wyoming Basin (Omernik)'),
    ('19E', 'Wasatch and Uinta Mountains (Omernik)'),
    ('19N', 'Colorado Plateau (TNC)'),
    ('20E', 'Colorado Plateau'),
    ('20E', 'Colorado Plateau (Omernik)'),
    ('21E', 'Southern Rockies (Omernik)'),
    ('22E', 'Arizona/New Mexico Plateau (Omernik)'),
    ('23E', 'Arizona/New Mexico Mountains (Omernik)'),
    ('23N', 'Sonoran Desert (TNC)'),
    ('24E', 'Chihuahuan Deserts (Omernik)'),
    ('25E', 'Western High Plains (Omernik)'),
    ('26E', 'Southwestern Tablelands (Omernik)'),
    ('79E', 'Madrean Archipelago (Omernik)'),
    ('80E', 'Northwestern Basin and Range (Omernik)'),
    ('81E', 'Sonoran Basin and Range (Omernik)'),
    ('9N', 'Utah-Wyoming Rocky Mountains (TNC)')]


def shipment_exists(field):
    if Shipment.select().where(Shipment.tracking_num == field.data).exists():
        raise validators.ValidationError('Shipment with that tracking number already exists.')


class AvailabilityForm(FlaskForm):
    accession = SelectField(
        'Accession',
        validators=[validators.input_required()],
        coerce=int
    )
    grin_avail = FloatField(
        'GRIN Availability in Grams'
    )
    bend_avail = FloatField(
        'Bend Availability in Grams'
    )
    cbg_avail = FloatField(
        'Chicago Botanic Garden Availability in Grams'
    )
    meeker_avail = FloatField(
        'Meeker Availability in Grams'
    )
    misc_avail = FloatField(
        'Miscellaneous Availability in Grams'
    )
    misc_inst_id = SelectField(
        'Miscellaneous Institute',
        coerce=int
    )
    ephraim_avail = FloatField(
        'Ephraim Availability in Grams'
    )
    nau_avail = FloatField(
        'Northern Arizona University Availability in Grams'
    )


class AccessionForm(FlaskForm):
    species = SelectField(
        'Species',
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
        validators=[validators.InputRequired(), validators.length(max=300)]
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
    # GeoLocation Fields
    phytoregion = SelectField(
        'Phytoregion Code',
        choices=PHYTOREGION_CODES,
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
    # GeoLocation Description Fields
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
        'Phone Extension',
        validators=[validators.optional()]
    )
    contact_email = StringField(
        'Contact Email',
        validators=[validators.Email()]
    )
    request_costs = BooleanField(
        'Request Costs?'
    )
    cost = FloatField(
        'Cost',
        validators=[validators.number_range(min=0.00, max=100.00)]
    )


class ReleaseForm(FlaskForm):
    species = SelectField(
        'Species'
    )
    accession = SelectField(
        'Accession'
    )
    loc_desc = TextAreaField(
        'GeoLocation Description'
    )
    germ_origin = StringField(
        'Germplasm origin',
        validators=[validators.length(max=100)]
    )
    name = StringField(
        'Release Name',
        validators=[validators.length(max=100)]
    )
    # This program is not designed to run past the year 4000
    year = IntegerField(
        'Year',
        validators=[validators.number_range(min=1800, max=4000)]
    )
    release_type = StringField(
        'Release Type',
        validators=[validators.length(max=100)]
    )
    plant_origin = StringField(
        'Plant Origin',
        validators=[validators.length(max=100)]
    )
    used_for = StringField(
        'Used For...',
        validators=[validators.length(max=300)]
    )
    select_criteria = StringField(
        'Selection Criteria',
        validators=[validators.length(max=200)]
    )
    special_character = StringField(
        'Special Characteristics',
        validators=[validators.length(max=200)]
    )
    adaptation = StringField(
        'Adaptation',
        validators=[validators.length(max=100)]
    )
    prime_pmc = StringField(
        'Prime Plant Materials Center',
        validators=[validators.length(max=100)]
    )
    primary_releasing = StringField(
        'Primary Releasing',
        validators=[validators.length(max=100)]
    )
    secondary_releasing = StringField(
        'Secondary Releasing',
        validators=[validators.length(max=100)]
    )
    cp_adapted = BooleanField(
        'Colorado Plateau Adapted?'
    )
    cp_sourced = BooleanField(
        'Colorado Plateau Sourced?'
    )
    source_num = StringField(
        'Source Number',
        validators=[validators.length(max=100)]
    )
    lb_acre_sow = FloatField(
        'Lbs Per Acre Sow'
    )
    lb_acre_yield = FloatField(
        'Lbs Per Acre Yield'
    )
    soil_adap = StringField(
        'Soil Adaptation',
        validators=[validators.length(max=100)]
    )
    precip_adap = StringField(
        'Precipitation Adaptation',
        validators=[validators.length(max=100)]
    )
    elev_adap = StringField(
        'Elevation Adaptation',
        validators=[validators.length(max=100)]
    )
    release_brochure = StringField(
        'Release Brochure',
        validators=[validators.url()]
    )
    comments = TextAreaField(
        'Comments',
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
        coerce=int
    )
    synonym = SelectField(
        'Synonym',
        validators=[validators.input_required()],
        coerce=int
    )


class TestingForm(FlaskForm):
    accession = SelectField(
        'Accession',
        validators=[validators.input_required()],
        coerce=int
    )
    entity = SelectField(
        'Entity',
        validators=[validators.input_required()],
        coerce=int
    )
    amt_rcvd_lbs = FloatField(
        'Amount Received (Lbs)'
    )
    clean_wt_lbs = FloatField(
        'Cleaned Weight (Lbs)'
    )
    est_seed_lb = FloatField(
        'Estimated Seed Per Pound'
    )
    est_pls_lb = FloatField(
        'Estimated Pure Live Seed Per Pound'
    )
    est_pls_collected = FloatField(
        'Estimated Pure Live Seed Collected'
    )
    test_type = SelectField(
        'Test Type',
        choices=[('XPC', 'XPC'), ('TZ', 'TZ'), ('XPMC', 'XPMC'), ('XRY', 'XRY')],
    )
    test_date = DateField(
        'Test Date'
    )
    purity = IntegerField(
        'Purity %',
        validators=[validators.number_range(min=0, max=100)]
    )
    tz = IntegerField(
        'TZ %',
        validators=[validators.number_range(min=0, max=100)]
    )
    fill = IntegerField(
        'Fill %',
        validators=[validators.number_range(min=0, max=100)]
    )


class UseForm(FlaskForm):
    accession = SelectField(
        'Accession',
        validators=[validators.input_required()],
        coerce=int
    )
    amount_gr = FloatField(
        'Amount in Grams'
    )
    purpose = TextAreaField(
        'Purpose',
        validators=[validators.input_required()]
    )
    date_start = DateField(
        'Date Start'
    )
    date_end = DateField(
        'Date End'
    )
    start_notes = TextAreaField(
        'Start Notes'
    )
    end_notes = TextAreaField(
        'End Notes'
    )
