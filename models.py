"""
CPNPP Database

Created:  4/13/2017
Updated:  5/15/2017
Author:   Avery Uslaner

This file holds the models and query logic for the database tables.
"""
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def add_column(table_name, column):
    column_name = column.compile(dialect=db.engine.dialect)
    column_type = column.type.compile(db.engine.dialect)
    db.session.execute('ALTER TABLE %s ADD COLUMN %s %s' % (table_name, column_name, column_type))


def compute_gr_to_lb(grams):
    return grams * 0.00220462


class Accession(db.Model):
    """
    The Accession table has a Many-to-One relationship with the Species 
    table.

    The Accession table has a One-to-Many relationship with the 
    Shipping table.

    The Accession table has a One-to-Many relationship with the Location
    table.

    The Accession table has a One-to-Many relationship with the Testing
    table.

    The Accession table has a One-to-One relationship with the
    Availability table.

    The Accession table has a One-to-Many relationship with the Use
    table.
    """
    __tablename__ = 'accession'

    id = db.Column(db.Integer, primary_key=True)
    data_source = db.Column(db.String(30))
    plant_habit = db.Column(db.String(30))  # Formerly Habit_rev
    coll_date = db.Column(db.DateTime)  # Sqlite expects YYYY-MM-DD format
    acc_num = db.Column(db.String(10))
    acc_num1 = db.Column(db.String(10))
    acc_num2 = db.Column(db.String(10))
    acc_num3 = db.Column(db.String(10))
    collected_with = db.Column(db.String(300))
    collection_misc = db.Column(db.Text)
    seed_source = db.Column(db.String(100))
    description = db.Column(db.Text)
    notes = db.Column(db.Text)
    increase = db.Column(db.Boolean)  # Slated for increase?

    # TODO: Link with storage locations

    species_id = db.Column(db.Integer, db.ForeignKey('species.id'))
    visit_id = db.Column(db.Integer, db.ForeignKey('visit.id'))

    species = db.relationship('Species', backref=db.backref('accessions', lazy='dynamic'), uselist=False)
    visits = db.relationship('Location', backref='accession')

    def __init__(
            self, data_source, plant_habit, coll_date, acc_num, acc_num1, acc_num2, acc_num3,
            collected_with, collection_misc, seed_source, description, notes, increase, species,
            location):
        self.data_source = data_source
        self.plant_habit = plant_habit
        self.coll_date = coll_date
        self.acc_num = acc_num
        self.acc_num1 = acc_num1
        self.acc_num2 = acc_num2
        self.acc_num3 = acc_num3
        self.collected_with = collected_with
        self.collection_misc = collection_misc
        self.seed_source = seed_source
        self.description = description
        self.notes = notes
        self.increase = increase
        self.species = species
        self.location = location

    def __repr__(self):
        return "<Accession(acc_num={})>".format(self.acc_num)


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


class Availability(db.Model):
    """
    The Availability table has a One-to-One relationship with the
    Accession table.

    The Availability table has a Many-to-One relationship with the
    Institution table.
    """
    __tablename__ = 'availability'

    id = db.Column(db.Integer, primary_key=True)
    grin_avail = db.Column(db.Float)
    bend_avail = db.Column(db.Float)
    cbg_avail = db.Column(db.Float)
    meeker_avail = db.Column(db.Float)
    misc_avail = db.Column(db.Float)
    ephraim_avail = db.Column(db.Float)
    nau_avail = db.Column(db.Float)
    avail_any = db.Column(db.Boolean)
    gr_avail = db.Column(db.Float)
    lb_avail = db.Column(db.Float)
    est_pls_avail = db.Column(db.Float)
    avail_no_grin = db.Column(db.Boolean)
    sum_gr_no_grin = db.Column(db.Float)
    sum_lb_no_grin = db.Column(db.Float)

    accession_id = db.Column(db.Integer, db.ForeignKey('accession.id'))
    misc_avail_id = db.Column(db.Integer, db.ForeignKey('institution.id'))

    accession = db.relationship('Accession', backref=db.backref('availability', uselist=False), uselist=False)
    misc_avail_inst = db.relationship('Institution', backref=db.backref('availability', lazy='dynamic'), uselist=False)

    def __init__(
            self, grin_avail, bend_avail, cbg_avail, meeker_avail, misc_avail, ephraim_avail,
            nau_avail, accession, misc_avail_inst):

        self.grin_avail = grin_avail
        self.bend_avail = bend_avail
        self.cbg_avail = cbg_avail
        self.meeker_avail = meeker_avail
        self.misc_avail = misc_avail
        self.ephraim_avail = ephraim_avail
        self.nau_avail = nau_avail
        self.accession = accession
        self.misc_avail_inst = misc_avail_inst

        self.gr_avail = self.compute_gr_avail()

        if self.check_avail_any():
            self.avail_any = 1
        else:
            self.avail_any = 0

        self.lb_avail = compute_gr_to_lb(self.gr_avail)

        # TODO
        # Implement method to compute est_pls_avail

        self.sum_gr_no_grin = self.compute_gr_no_grin()

        if self.check_avail_no_grin():
            self.avail_no_grin = 1
        else:
            self.avail_no_grin = 0

        self.sum_lb_no_grin = compute_gr_to_lb(self.sum_gr_no_grin)

    def __repr__(self):
        return ("<Availability(accession={}, avail_any={}, est_pls_avail={}, avail_no_grin={}, "
                "grin_avail={}, bend_avail={}, cbg_avail={}, meeker_avail={})>".format(
            self.accession, self.avail_any, self.est_pls_avail, self.avail_no_grin,
            self.grin_avail, self.bend_avail, self.cbg_avail, self.meeker_avail))

    def check_avail_any(self):
        if self.gr_avail > 0:
            return True
        else:
            return False

    def check_avail_no_grin(self):
        if self.sum_gr_no_grin > 0:
            return True
        else:
            return False

    def compute_gr_avail(self):
        return (self.grin_avail + self.bend_avail + self.cbg_avail + self.meeker_avail +
                self.misc_avail + self.ephraim_avail + self.nau_avail)

    def compute_gr_no_grin(self):
        return (self.bend_avail + self.cbg_avail + self.meeker_avail + self.misc_avail +
                self.ephraim_avail + self.nau_avail)


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

    address = db.relationship('Address', backref='contacts')
    institute = db.relationship('Institution', backref='contacts')

    def __init__(self, first_name, last_name, email, telephone, tel_ext, title, agency, address, institute):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.telephone = telephone
        self.tel_ext = tel_ext
        self.title = title
        self.agency = agency
        self.address = address
        self.institute = institute

    def __repr__(self):
        return "<Contact(first_name={}, last_name={})>".format(
            self.first_name, self.last_name)


class Institution(db.Model):
    """
    The Institution table has a One-to-Many relationship with the
    Shipping table.

    The Institution table has a One-to-Many relationship with the
    Address table.

    The Institution table has a One-to-Many relationship with the
    Contact table.
    """
    __tablename__ = 'institution'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    # General phone number that may or may not be related to particular contact
    institute_phone = db.Column(db.Integer)
    institute_phone_ext = db.Column(db.Integer)
    # General email that may or may not be related to a particular contact
    institute_email = db.Column(db.String(50))
    request_costs = db.Column(db.Boolean)  # Does this institution charge a fee for requesting seed?
    # If we need to calculate things by cost, store dollars and cents separately
    cost = db.Column(db.Float)  # How much?

    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))

    address = db.relationship('Address', backref='institute', uselist=False)

    def __init__(
            self, name, institute_phone, institute_phone_ext, institute_email,
            request_costs, cost, address):
        self.name = name
        self.institute_phone = institute_phone
        self.institute_phone_ext = institute_phone_ext
        self.institute_email = institute_email
        self.request_costs = request_costs
        self.cost = cost
        self.address = address

    def __repr__(self):
        return "<Institution(name={}, address={})>".format(
            self.name, self.address)


class Release(db.Model):
    """
    Release table has a Many-to-One relationship with the
    Accession table.

    Release table has a Many-to-One relationship with the
    Species table.
    """
    __tablename__ = 'release'

    id = db.Column(db.Integer, primary_key=True)
    loc_desc = db.Column(db.Text)  # When a more specific location_id is not available
    germ_origin = db.Column(db.String(100))
    name = db.Column(db.String(100))
    year = db.Column(db.Integer)
    release_type = db.Column(db.String(100))
    plant_origin = db.Column(db.String(100))
    used_for = db.Column(db.String(300))
    select_criteria = db.Column(db.String(200))
    special_character = db.Column(db.String(200))
    adaptation = db.Column(db.String(100))
    prime_pmc = db.Column(db.String(100))
    primary_releasing = db.Column(db.String(100))
    secondary_releasing = db.Column(db.String(100))
    cp_adapted = db.Column(db.Boolean)
    cp_sourced = db.Column(db.Boolean)
    source_num = db.Column(db.String(100))
    lb_acre_sow = db.Column(db.Float)
    lb_acre_yield = db.Column(db.Float)
    soil_adap = db.Column(db.String(100))
    precip_adap = db.Column(db.String(100))
    elev_adap = db.Column(db.String(100))
    release_brochure = db.Column(db.String(200))
    comments = db.Column(db.Text)

    accession_id = db.Column(db.Integer, db.ForeignKey('accession.id'))
    species_id = db.Column(db.Integer, db.ForeignKey('species.id'))

    accession = db.relationship('Accession', backref='releases', uselist=False)
    species = db.relationship('Species', backref=db.backref('releases', lazy='dynamic'), uselist=False)

    def __init__(
            self, loc_desc, germ_origin, name, year, release_type, plant_origin,
            used_for, select_criteria, special_character, adaptation, prime_pmc,
            primary_releasing, secondary_releasing, cp_adapted, cp_sourced,
            source_num, lb_acre_sow, lb_acre_yield, soil_adap, precip_adap,
            elev_adap, release_brochure, comments, accession, species):

        self.loc_desc = loc_desc
        self.germ_origin = germ_origin
        self.name = name
        self.year = year
        self.release_type = release_type
        self.plant_origin = plant_origin
        self.used_for = used_for
        self.select_criteria = select_criteria
        self.special_character = special_character
        self.adaptation = adaptation
        self.prime_pmc = prime_pmc
        self.primary_releasing = primary_releasing
        self.secondary_releasing = secondary_releasing
        self.cp_adapted = cp_adapted
        self.cp_sourced = cp_sourced
        self.source_num = source_num
        self.lb_arce_sow = lb_acre_sow
        self.lb_acre_yield = lb_acre_yield
        self.soil_adap = soil_adap
        self.precip_adap = precip_adap
        self.elev_adap = elev_adap
        self.release_brochure = release_brochure
        self.comments = comments
        self.accession = accession
        self.species = species

    def __repr__(self):
        return ("<Release(loc_desc={}, germ_origin={}, name={}, year={}, release_type={}, "
                "lb_arce_sow={}, lb_acre_yield={})>".format(self.loc_desc, self.germ_origin,
                                                            self.name, self.year,
                                                            self.release_type, self.lb_arce_sow,
                                                            self.lb_acre_yield))


class Shipping(db.Model):
    """
    The Shipping table has a Many-to-One relationship with the 
    Institution table.

    The Shipping table has a Many-to-One relationship with the Accession
    table.

    A shipment also maintains multiple ForeignKey fields to the 
    Institution table for both the origin institute and the destination 
    institute.

    [?] http://docs.sqlalchemy.org/en/rel_0_9/orm/join_conditions.html#handling-multiple-join-paths
    """
    __tablename__ = 'shipping'

    id = db.Column(db.Integer, primary_key=True)
    ship_date = db.Column(db.DateTime)
    tracking_num = db.Column(db.String(25), unique=True)
    tracking_num_comp = db.Column(db.String(30))  # E.g. Fedex
    amount_gr = db.Column(db.Float)
    amount_lb = db.Column(db.Float)
    amount_perc = db.Column(db.Float)
    calc_by = db.Column(db.String(30))  # Was amount calculated by counting or weight?

    origin_institute_id = db.Column(db.Integer, db.ForeignKey('institution.id'))
    destination_institute_id = db.Column(db.Integer, db.ForeignKey('institution.id'))
    accession_id = db.Column(db.Integer, db.ForeignKey('accession.id'))

    origin_institute = db.relationship('Institution', foreign_keys=[origin_institute_id])
    destination_institute = db.relationship('Institution', foreign_keys=[destination_institute_id])
    accession = db.relationship('Accession', backref='shipments')

    def __init__(
            self, ship_date, tracking_num, tracking_num_comp, amount_gr, calc_by, origin_institute,
            destination_institute, accession):
        self.ship_date = ship_date
        self.tracking_num = tracking_num
        self.tracking_num_comp = tracking_num_comp
        self.amount_gr = amount_gr
        self.calc_by = calc_by
        self.origin_institute = origin_institute
        self.destination_institute = destination_institute
        self.accession = accession

        # TODO Create method to calculate amount_perc

        self.amount_lb = compute_gr_to_lb(amount_gr)

    def __repr__(self):
        return ("<Shipping(ship_date={}, tracking_num={}, amount_gr={}, "
                "amount_perc={}, calc_by={})>".format(
            self.ship_date, self.tracking_num, self.amount_gr,
            self.amount_perc, self.calc_by))


class Species(db.Model):
    """
    The Species table has a One-to-Many relationship with other objects
    in the same table.
    
    [?] http://docs.sqlalchemy.org/en/rel_1_1/orm/self_referential.html#adjacency-list-relationships
    
    The Species table has a One-to-Many relationship with the Accession
    table.
    """
    __tablename__ = 'species'

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), unique=True)
    name_full = db.Column(db.String(100), unique=True)
    common = db.Column(db.String(50))
    family = db.Column(db.String(30))
    genus = db.Column(db.String(30))
    species = db.Column(db.String(30))
    var_ssp1 = db.Column(db.String(30))
    var_ssp2 = db.Column(db.String(30))
    plant_type = db.Column(db.String(30))
    plant_duration = db.Column(db.String(30))
    priority_species = db.Column(db.Boolean)
    gsg_val = db.Column(db.Boolean)
    poll_val = db.Column(db.Boolean)
    research_val = db.Column(db.Boolean)

    parent_id = db.Column(db.Integer, db.ForeignKey('species.id'))
    synonyms = db.relationship('Species', backref=db.backref('usda_name', remote_side=[id]))

    def __init__(
            self, symbol, name_full, common, family, genus, species, var_ssp1, var_ssp2, plant_type,
            plant_duration, priority_species, gsg_val, poll_val, research_val, parent_id=None,
            synonyms=None):

        self.symbol = symbol
        self.name_full = name_full
        self.common = common
        self.family = family
        self.genus = genus
        self.species = species
        self.var_ssp1 = var_ssp1
        self.var_ssp2 = var_ssp2
        self.plant_type = plant_type
        self.plant_duration = plant_duration
        self.priority_species = priority_species
        self.gsg_val = gsg_val
        self.poll_val = poll_val
        self.research_val = research_val

        if parent_id:
            self.parent_id = parent_id

        if synonyms:
            self.synonyms = synonyms

    def __repr__(self):
        return "<Species(symbol={}, name_full={})>".format(
            self.symbol, self.name_full)

    def add_synonym(self, plant):
        self.synonyms.append(plant)


storage_locations = db.Table(
    'storage_locations',
    db.Column('institute_id', db.Integer, db.ForeignKey('institution.id')),
    db.Column('accession_id', db.Integer, db.ForeignKey('accession.id')))


class Testing(db.Model):
    """
    The Testing table has a Many-to-One relationship with the 
    Accession table.
    """
    __tablename__ = 'test'

    id = db.Column(db.Integer, primary_key=True)
    amt_rcvd_lbs = db.Column(db.Float)
    clean_wt_lbs = db.Column(db.Float)
    est_seed_lb = db.Column(db.Float)  # Estimated seeds per pound
    est_pls_lb = db.Column(db.Float)  # Estimated Pure Live Seed per pound
    est_pls_collected = db.Column(db.Float)
    test_type = db.Column(db.String(30))
    test_date = db.Column(db.DateTime)
    purity = db.Column(db.Integer)
    tz = db.Column(db.Integer)
    fill = db.Column(db.Integer)

    accession_id = db.Column(db.Integer, db.ForeignKey('accession.id'))

    accession = db.relationship('Accession', backref=db.backref('tests', lazy='dynamic'), uselist=False)

    def __init__(
            self, amt_rcvd_lbs, clean_wt_lbs, est_seed_lb, est_pls_lb, est_pls_collected,
            test_type, test_date, purity, tz, fill, accession):

        self.amt_rcvd_lbs = amt_rcvd_lbs
        self.clean_wt_lbs = clean_wt_lbs
        self.est_seed_lb = est_seed_lb
        self.est_pls_lb = est_pls_lb
        self.est_pls_collected = est_pls_collected
        self.test_type = test_type
        self.test_date = test_date
        self.purity = purity
        self.tz = tz
        self.fill = fill
        self.accession = accession

    def __repr__(self):
        return ("<Testing(accession={}, amt_rcvd_lbs={}, clean_wt_lbs={}, est_seed_lb={}, "
                "est_pls_lb={}, est_pls_collected={}, purity={}, tz={})>".format(
                    self.accession, self.amt_rcvd_lbs, self.clean_wt_lbs, self.est_seed_lb,
                    self.est_pls_lb, self.est_pls_collected, self.purity, self.tz))


class Use(db.Model):
    """
    Use table has a Many-to-One relationship with the Accession table.

    Use table has a Many-to-One relationship with the Species table.
    
    Use table has a One-to-One relationship with the Institution table.
    
    Use table has a One-to-Many relationship with the Contact table.
    """
    __tablename__ = 'use'

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(50))
    amount_gr = db.Column(db.Float)
    amount_lb = db.Column(db.Float)
    purpose = db.Column(db.Text)
    date_start = db.Column(db.DateTime)
    date_end = db.Column(db.DateTime)
    start_notes = db.Column(db.Text)
    end_notes = db.Column(db.Text)

    accession_id = db.Column(db.Integer, db.ForeignKey('accession.id'))
    species_id = db.Column(db.Integer, db.ForeignKey('species.id'))
    institute_id = db.Column(db.Integer, db.ForeignKey('institution.id'))
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))

    accession = db.relationship('Accession', backref='uses', uselist=False)
    species = db.relationship('Species', backref=db.backref('uses', lazy='dynamic'), uselist=False)
    institute = db.relationship('Institution', backref=db.backref('uses', lazy='dynamic'), uselist=False)
    contacts = db.relationship('Contact')

    def __init__(
            self, project_name, amount_gr, purpose, date_start, date_end, start_notes, end_notes, accession, species,
            institute, contacts):
        self.project_name = project_name
        self.amount_gr = amount_gr
        self.purpose = purpose
        self.date_start = date_start
        self.date_end = date_end
        self.start_notes = start_notes
        self.end_notes = end_notes
        self.accession = accession
        self.species = species
        self.institute = institute
        self.contacts = contacts

        self.amount_lb = compute_gr_to_lb(amount_gr)

    def __repr__(self):
        return ("<Use(project_name={}, amount_gr={}, amount_lb={}, amount_perc={}, "
                "purpose={}, date_start={}, date_end={})>".format(
            self.project_name, self.amount_gr, self.amount_lb, self.amount_perc,
            self.purpose, self.date_start, self.date_end))


class Location(db.Model):
    """
    The Location table has a One-to-One relationship with the Accession
    table.

    The Location table has a One-to-Many relationship with the 
    Visit table.

    The Location table has a One-to-One relationship with the Zone
    table.
    """
    __tablename__ = 'location'

    id = db.Column(db.Integer, primary_key=True)
    land_owner = db.Column(db.String(30))
    geology = db.Column(db.String(100))
    soil_type = db.Column(db.String(100))
    phytoregion = db.Column(db.String(30))
    phytoregion_full = db.Column(db.String(50))
    # locality of the collection site if applicable - i.e. National Forest/NCA's, etc.
    locality = db.Column(db.String(50))  # Formerly SUB_CNT3
    geog_area = db.Column(db.String(50))
    directions = db.Column(db.Text)  # Formerly locality
    degrees_n = db.Column(db.Integer)
    minutes_n = db.Column(db.Integer)
    seconds_n = db.Column(db.Float)
    degrees_w = db.Column(db.Integer)
    minutes_w = db.Column(db.Integer)
    seconds_w = db.Column(db.Float)
    latitude_decimal = db.Column(db.Float)
    longitude_decimal = db.Column(db.Float)
    georef_source = db.Column(db.String(50))
    gps_datum = db.Column(db.String(10))
    altitude = db.Column(db.Integer)
    altitude_unit = db.Column(db.String(10))
    altitude_in_m = db.Column(db.Integer)
    fo_name = db.Column(db.String(50))
    district_name = db.Column(db.String(50))
    state = db.Column(db.String(20))
    county = db.Column(db.String(30))

    visit_description_id = db.Column(db.Integer, db.ForeignKey('visit.id'))
    zone_id = db.Column(db.Integer, db.ForeignKey('zone.id'))

    zone = db.relationship('Zone', uselist=False)
    visit_descriptions = db.relationship('Visit')

    def __init__(
            self, land_owner, geology, soil_type, phytoregion, phytoregion_full, locality, geog_area, directions,
            degrees_n, minutes_n, seconds_n, degrees_w, minutes_w, seconds_w, latitude_decimal,
            longitude_decimal, georef_source, gps_datum, altitude, altitude_unit,
            altitude_in_m, fo_name, district_name, state, county, visit_descriptions, zone):
        self.land_owner = land_owner
        self.geology = geology
        self.soil_type = soil_type
        self.phytoregion = phytoregion
        self.phytoregion_full = phytoregion_full
        self.locality = locality
        self.geog_area = geog_area
        self.directions = directions
        self.degrees_n = degrees_n
        self.minutes_n = minutes_n
        self.seconds_n = seconds_n
        self.degrees_w = degrees_w
        self.minutes_w = minutes_w
        self.seconds_w = seconds_w
        self.latitude_decimal = latitude_decimal
        self.longitude_decimal = longitude_decimal
        self.georef_source = georef_source
        self.gps_datum = gps_datum
        self.altitude = altitude
        self.altitude_unit = altitude_unit
        self.altitude_in_m = altitude_in_m
        self.fo_name = fo_name
        self.district_name = district_name
        self.state = state
        self.county = county
        self.visit_descriptions = visit_descriptions
        self.zone = zone

    def __repr__(self):
        return "<Location(latitude_decimal={}, longitude_decimal={})>".format(
            self.latitude_decimal, self.longitude_decimal)


class Visit(db.Model):
    """
    The Visit table has a Many-to-One relationship with the Accession 
    table.
    
    The Visit table has a Many-to-One relationship with the Location
    table.
    """
    __tablename__ = 'visit'

    id = db.Column(db.Integer, primary_key=True)
    associated_taxa_full = db.Column(db.Text)
    mod = db.Column(db.String(200))   # modifying factors of collection site (grazed, etc.)
    mod2 = db.Column(db.String(200))  # additional modifying factors of collection site (roadside, etc.)
    geomorphology = db.Column(db.String(100))
    slope = db.Column(db.String(30))
    aspect = db.Column(db.String(10))
    habitat = db.Column(db.String(100))
    population_size = db.Column(db.Integer)
    occupancy = db.Column(db.Integer)  # Number of plants collected from

    def __init__(
            self, associated_taxa_full, mod, mod2, geomorphology, slope, aspect, habitat, population_size, occupancy):
        self.associated_taxa_full = associated_taxa_full
        self.mod = mod
        self.mod2 = mod2
        self.geomorphology = geomorphology
        self.slope = slope
        self.aspect = aspect
        self.habitat = habitat
        self.population_size = population_size
        self.occupancy = occupancy

    def __repr__(self):
        return "<Visit(land_owner={}, population_size={})>".format(
            self.land_owner, self.population_size)


class Zone(db.Model):
    """
    The Zone table has a One-to-One relationship with the Accession
    table.
    """
    __tablename__ = 'zone'

    id = db.Column(db.Integer, primary_key=True)
    ptz = db.Column(db.String(30))
    us_l4_code = db.Column(db.String(10))
    us_l4_name = db.Column(db.String(30))
    us_l3_code = db.Column(db.String(10))
    us_l3_name = db.Column(db.String(30))
    achy_sz_gridcode = db.Column(db.Integer)  # Achnatherum hymenoides
    achy_sz_zone = db.Column(db.String(10))
    aslo3_sz_gridcode = db.Column(db.Integer)  # Astragalus lonchocarpus
    aslo3_sz_zone = db.Column(db.String(10))
    bogr2_sz_gridcode = db.Column(db.Integer)  # Bouteloua gracilis
    bogr2_sz_zone = db.Column(db.String(10))
    cllu2_sz_gridcode = db.Column(db.Integer)  # Cleome lutea
    cllu2_sz_zone = db.Column(db.String(10))
    elel5_sz_gridcode = db.Column(db.Integer)  # Elymus elymoides
    elel5_sz_zone = db.Column(db.String(10))
    maca2_sz_gridcode = db.Column(db.Integer)  # Machaeranthera canescens
    maca2_sz_zone = db.Column(db.String(10))
    plja_sz_gridcode = db.Column(db.Integer)  # Pleuraphis jamesii
    plja_sz_zone = db.Column(db.String(10))
    sppa2_sz_gridcode = db.Column(db.Integer)  # Sphaeralcea parvifolia
    sppa2_sz_zone = db.Column(db.String(10))
    spcr_sz_gridcode = db.Column(db.Integer)  # Sporobolus cryptandrus
    spcr_sz_zone = db.Column(db.String(10))
    cp_buff = db.Column(db.Boolean)
    cp_strict = db.Column(db.Boolean)
    avail_buff = db.Column(db.Boolean)
    avail_strict = db.Column(db.Boolean)
    usgs_zone = db.Column(db.Integer)

    def __init__(
            self, ptz, us_l4_code, us_l4_name, us_l3_code, us_l3_name, achy_sz_gridcode,
            achy_sz_zone, aslo3_sz_gridcode, aslo3_sz_zone, bogr2_sz_gridecode, bogr2_sz_zone, cllu2_sz_gridcode,
            cllu2_sz_zone, elel5_sz_gridcode, elel5_sz_zone, maca2_sz_gridcode, maca2_sz_zone, plja_sz_gridcode,
            plja_sz_zone, sppa2_sz_gridcode, sppa2_sz_zone, cp_buff, cp_strict, avail_buff, avail_strict, usgs_zone):

        self.ptz = ptz
        self.us_l4_code = us_l4_code
        self.us_l4_name = us_l4_name
        self.us_l3_code = us_l3_code
        self.us_l3_name = us_l3_name
        self.achy_sz_gridcode = achy_sz_gridcode
        self.achy_sz_zone = achy_sz_zone
        self.aslo3_sz_gridcode = aslo3_sz_gridcode
        self.aslo3_sz_zone = aslo3_sz_zone
        self.bogr2_sz_gridcode = bogr2_sz_gridecode
        self.bogr2_sz_zone = bogr2_sz_zone
        self.cllu2_sz_gridcode = cllu2_sz_gridcode
        self.cllu2_sz_zone = cllu2_sz_zone
        self.elel5_sz_gridcode = elel5_sz_gridcode
        self.elel5_sz_zone = elel5_sz_zone
        self.maca2_sz_gridcode = maca2_sz_gridcode
        self.maca2_sz_zone = maca2_sz_zone
        self.plja_sz_gridcode = plja_sz_gridcode
        self.plja_sz_zone = plja_sz_zone
        self.sppa2_sz_gridcode = sppa2_sz_gridcode
        self.sppa2_sz_zone = sppa2_sz_zone
        self.cp_buff = cp_buff
        self.cp_strict = cp_strict
        self.avail_buff = avail_buff
        self.avail_strict = avail_strict
        self.usgs_zone = usgs_zone

    def __repr__(self):
        return "<Zone(ptz={})>".format(self.ptz)
