#!/usr/bin/python
# coding=utf-8

import datetime
import unittest

from app import app
from models import (db, Accession, Address, AmountUsed, Availability, Contact, Entity, GeoLocation, Release, SeedUse,
                    Shipment, Species, Testing, Visit, Zone)


def create_app():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    db.init_app(app)
    return app


class AccessionTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        db.create_all()
        self.plant = Species(symbol='ABAB', name_full='Abutilon abutiloides', common='shrubby Indian mallow',
                        family='Malvaceae', genus='Abutilon', species='abutiloides', var_ssp1=None, var_ssp2=None,
                        plant_type=None, plant_duration=None, priority_species=0, gsg_val=0,
                        poll_val=0, research_val=0)
        self.synonym1 = Species(symbol='ABAM5', name_full='Abutilon americanum', common='shrubby Indian mallow',
                           family='Malvaceae', genus='Abutilon', species='americanum', var_ssp1=None, var_ssp2=None,
                           plant_type=None, plant_duration=None, priority_species=0, gsg_val=0,
                           poll_val=0, research_val=0)
        self.synonym2 = Species(symbol='ABJA', name_full='Abutilon jacquinii', common='shrubby Indian mallow',
                           family='Malvaceae', genus='Abutilon', species='jacquinii', var_ssp1=None, var_ssp2=None,
                           plant_type=None, plant_duration=None, priority_species=0, gsg_val=0,
                           poll_val=0, research_val=0)
        self.synonym3 = Species(symbol='ABLA', name_full='Abutilon lignosum', common='shrubby Indian mallow',
                           family='Malvaceae', genus='Abutilon', species='lignosum', var_ssp1=None, var_ssp2=None,
                           plant_type=None, plant_duration=None, priority_species=0, gsg_val=0,
                           poll_val=0, research_val=0)
        self.address1 = Address(address_one='P.O. Box 1029', address_two='1117 N. Main Street', state='UT', city='Monticello',
                          zipcode=84535)
        self.address2 = Address(address_one='271 W Bitterbrush Lane (aka Prison Road)', address_two='Green Building',
                           city='Draper', state='UT', zipcode=840209599)
        self.contact1 = Contact(first_name='Mark', last_name='Grover', email='mgrover@fourcornersschool.org',
                          telephone=4355872156, tel_ext=1024, title='Conservation Coordinator', agency=None,
                          address=address)
        self.contact2 = Contact(first_name='Tom', last_name='Glass', email='tom@highmtnnursery.com', telephone=2084216904,
                            tel_ext=None, title='Owner', address=address2)
        self.entity1 = Entity(name='Four Corners School of Outdoor Education', address=address, contacts=contact,
                         request_costs=1, cost=35.00, entity_email='info@fourcornersschool.org',
                         entity_phone=4355872156, entity_phone_ext=1010)
        self.entity2 = Entity(name='High Mountain Nursery', address=address2, contacts=contact_2, request_costs=0, cost=None,
                         )
        self.visit1 = Visit(date=datetime.date.today(), associated_taxa_full=('Quercus gambelii, Ericameria nauseosa '
                                                                              'ssp. consimilis var. nitida, Artemisia '
                                                                              'tridentata ssp. wyomingensis, Lepidium '
                                                                              'sp.:Rosa woodsii, Heterotheca villosa '
                                                                              'var. villosa:Carex geyeri, Koeleria '
                                                                              'macrantha'),
                            mod='grazed, trampled', mod2='recreation', geomorphology=None, slope='5-25 degrees',
                            aspect='varied', habitat='Mountain Brush; meadow along road', population_size=200,
                            accession=None)
        self.zone = Zone(ptz='10 - 15 Deg. F./6 - 12', us_l4_code='20c',
                    us_l4_name='Semiarid Benchlands and Canyonlands',
                    us_l3_code='20', us_l3_name='Colorado Plateaus',
                    achy_sz_gridcode=11, achy_sz_zone='L1L2H3', cp_buff=1, cp_strict=1, avail_buff=1,
                    avail_strict=0, usgs_zone=0)
        self.location = GeoLocation(phytoregion='25E', phytoregion_full='Western High Plains (Omernik)',
                               locality='Grand Staircase Escalante National Monument',
                               geog_area='Big Cottonwood Canyon',
                               directions=('Head NE on HWY 62/180 for 30 miles and turn left on '
                                           'county road 243. Continue on 243 for 8.3 miles then turn '
                                           'left onto county toad 126A. Continue on 126A for 12 miles '
                                           'then turn right. Continue for approximately 1.1 miles to '
                                           'reach collection site.'),
                               degrees_n=38, minutes_n=20, seconds_n=16.32, degrees_w=107, minutes_w=53,
                               seconds_w=59.64, latitude_decimal=38.33786, longitude_decimal=-107.8999,
                               georef_source='GPS', gps_datum='NAD83', altitude=7100, altitude_unit='ft',
                               altitude_in_m=2164, fo_name='UNCOMPAHGRE FIELD OFFICE',
                               district_name='SOUTHWEST DISTRICT OFFICE', state='CO', county='Montrose',
                               location_description=desc, zone=zone)
        self.accession = Accession(data_source='UP', plant_habit='Forb/herb',
                              coll_date=datetime.date(year=2004, month=8, day=24), acc_num='UP-76',
                              acc_num1='UP', acc_num2='76', acc_num3=None,
                              collected_with='GVR, CH, SP',
                              collection_misc=('Hand-pick ripe seeds, all stages still on plants.'
                                               'This Aster glaucodes is in a nice loamy field (not rocky cliff '
                                               'like other Aster glaucodes)'), seed_source='P',
                              description='Height: 0.15-0.45 m',
                              notes=('Official SOS collection number is NM930N-69: details '
                                     'submitted to SOS National Office by Farmington BLM Botanist.  '
                                     'Germination and competition trials for early seral species '
                                     '(Chicago Botanic Garden).  Photos of habitat, plant and seed'),
                              increase=0, species=plant, location=location)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.plant = None
        self.synonym1 = None
        self.synonym2 = None
        self.synonym3 = None
        self.address1 = None
        self.address2 = None
        self.contact1 = None
        self.contact2 = None
        self.entity1 = None
        self.entity2 = None
        self.visit1 = None
        self.visit2 = None
        self.zone1 = None
        self.zone2 = None
        self.location1 = None
        self.location2 = None
        self.accession1 = None
        self.accession2 = None

    def test_species_synonym_relationship(self):
        self.plant.add_synonym(self.synonym1)
        self.plant.add_synonym(self.synonym2)
        self.plant.add_synonym(self.synonym3)
        db.session.add(self.synonym1)
        db.session.add(self.synonym2)
        db.session.add(self.synonym3)
        db.session.add(self.plant)
        db.session.commit()
        self.assertEqual(len(self.plant.synonyms), 3)
        self.assertEqual(self.synonym1.usda_name, self.plant)
        self.assertEqual(self.synonym2.usda_name, self.plant)
        self.assertEqual(self.synonym3.usda_name, self.plant)

    def test_shipment_accession_relationship(self):
        db.session.add(institute1)
        db.session.add(institute2)
        db.session.add(plant)
        db.session.add(desc)
        db.session.add(zone)
        db.session.add(location)
        db.session.add(accession)
        shipment = Shipment(ship_date=datetime.datetime.now(), tracking_num='40012345678',
                            tracking_num_comp='FedEx', amount_gr=0.60847634, calc_by='counting',
                            origin_institute=institute1, destination_institute=institute2,
                            accession=accession)
        db.session.add(shipment)
        db.session.commit()
        self.assertEqual(shipment.accession, accession)
        self.assertEqual(shipment.accession_id, accession.id)
        self.assertIn(shipment, accession.shipments)

    def test_shipment_institute_relationship(self):
        institute1 = Entity(name='Four Corners School of Outdoor Education',
                            address='P.O. Box 1029\n1117 N. Main Street\nMonticello, UT 84535',
                            contact_name='Mark Grover', contact_phone=4355872156,
                            contact_phone_ext=1024, contact_email='mgrover@fourcornersschol.org',
                            request_costs='No')
        institute2 = Entity(name='High Mountain Nursery',
                            address=('271 W Bitterbrush Lane (aka Prison Road)\nGreen Building\n'
                                          'Draper, UT 84020-9599'), contact_name='Tom Glass',
                            contact_phone=2084216904,
                            contact_phone_ext=None, contact_email='tom@highmtnnursery.com',
                            request_costs='No')
        desc = GeoLocationDescription(land_owner='BLM',
                                      associated_taxa_full=('Quercus gambelii:'
                                                         'Ericameria nauseosa ssp. consimilis var. '
                                                         'nitida:Artemisia tridentata ssp. '
                                                         'wyomingensis:Lepidium sp.:Rosa woodsii:'
                                                         'Heterotheca villosa var. villosa:Carex '
                                                         'geyeri:Koeleria macrantha'),
                                      mod='grazed, trampled', mod2='recreation', geomorphology=None,
                                      slope='5-25 degrees', aspect='varied',
                                      habitat='Mountain Brush; meadow along road',
                                      geology='Quaternary, alluvial deposits',
                                      soil_type='Asphalt and sand, tan/red',
                                      population_size=200, occupancy=1500)
        zone = Zone(ptz='10 - 15 Deg. F./6 - 12', us_l4_code='20c',
                    us_l4_name='Semiarid Benchlands and Canyonlands',
                    us_l3_code='20', us_l3_name='Colorado Plateaus',
                    achy_sz_gridcode=11, achy_sz_zone='L1L2H3', cp_buff=1, cp_strict=1, avail_buff=1,
                    avail_strict=0, usgs_zone=0)
        location = GeoLocation(phytoregion='25E', phytoregion_full='Western High Plains (Omernik)',
                               locality='Grand Staircase Escalante National Monument',
                               geog_area='Big Cottonwood Canyon',
                               directions=('Head NE on HWY 62/180 for 30 miles and turn left on '
                                        'county road 243. Continue on 243 for 8.3 miles then turn '
                                        'left onto county toad 126A. Continue on 126A for 12 miles '
                                        'then turn right. Continue for approximately 1.1 miles to '
                                        'reach collection site.'),
                               degrees_n=38, minutes_n=20, seconds_n=16.32, degrees_w=107, minutes_w=53,
                               seconds_w=59.64, latitude_decimal=38.33786, longitude_decimal=-107.8999,
                               georef_source='GPS', gps_datum='NAD83', altitude=7100, altitude_unit='ft',
                               altitude_in_m=2164, fo_name='UNCOMPAHGRE FIELD OFFICE',
                               district_name='SOUTHWEST DISTRICT OFFICE', state='CO', county='Montrose',
                               location_description=desc, zone=zone)
        plant = Species(symbol='ABAB', name_full='Abutilon abutiloides', common='shrubby Indian mallow',
                        family='Malvaceae', genus='Abutilon', species='abutiloides', var_ssp1=None, var_ssp2=None,
                        plant_type=None, plant_duration=None, priority_species=0, gsg_val=0,
                        poll_val=0, research_val=0)
        accession = Accession(data_source='UP', plant_habit='Forb/herb',
                              coll_date=datetime.date(year=2004, month=8, day=24), acc_num='UP-76',
                              acc_num1='UP', acc_num2='76', acc_num3=None,
                              collected_with='GVR, CH, SP',
                              collection_misc=('Hand-pick ripe seeds, all stages still on plants.'
                                               'This Aster glaucodes is in a nice loamy field (not rocky cliff '
                                               'like other Aster glaucodes)'), seed_source='P',
                              description='Height: 0.15-0.45 m',
                              notes=('Official SOS collection number is NM930N-69: details '
                                     'submitted to SOS National Office by Farmington BLM Botanist.  '
                                     'Germination and competition trials for early seral species '
                                     '(Chicago Botanic Garden).  Photos of habitat, plant and seed'),
                              increase=0, species=plant, location=location)
        db.session.add(institute1)
        db.session.add(institute2)
        db.session.add(plant)
        db.session.add(desc)
        db.session.add(zone)
        db.session.add(location)
        db.session.add(accession)
        shipment = Shipment(ship_date=datetime.datetime.now(), tracking_num='40012345678',
                            tracking_num_comp='FedEx', amount_gr=0.60847634, calc_by='counting',
                            origin_institute=institute1, destination_institute=institute2,
                            accession=accession)
        db.session.add(shipment)
        db.session.commit()
        self.assertEqual(shipment.amount_lb, 0.60847634 * 0.00220462)
        self.assertEqual(shipment.origin_institute, institute1)
        self.assertEqual(shipment.destination_institute, institute2)

    def test_accession_location_relationship(self):
        plant = Species(symbol='ABAB', name_full='Abutilon abutiloides', common='shrubby Indian mallow',
                        family='Malvaceae', genus='Abutilon', species='abutiloides', var_ssp1=None, var_ssp2=None,
                        plant_type=None, plant_duration=None, priority_species=0, gsg_val=0,
                        poll_val=0, research_val=0)
        desc = GeoLocationDescription(land_owner='BLM',
                                      associated_taxa_full=('Quercus gambelii:'
                                                         'Ericameria nauseosa ssp. consimilis var. '
                                                         'nitida:Artemisia tridentata ssp. '
                                                         'wyomingensis:Lepidium sp.:Rosa woodsii:'
                                                         'Heterotheca villosa var. villosa:Carex '
                                                         'geyeri:Koeleria macrantha'),
                                      mod='grazed, trampled', mod2='recreation', geomorphology=None,
                                      slope='5-25 degrees', aspect='varied',
                                      habitat='Mountain Brush; meadow along road',
                                      geology='Quaternary, alluvial deposits',
                                      soil_type='Asphalt and sand, tan/red',
                                      population_size=200, occupancy=1500)
        zone = Zone(ptz='10 - 15 Deg. F./6 - 12', us_l4_code='20c',
                    us_l4_name='Semiarid Benchlands and Canyonlands',
                    us_l3_code='20', us_l3_name='Colorado Plateaus',
                    achy_sz_gridcode=11, achy_sz_zone='L1L2H3', cp_buff=1, cp_strict=1, avail_buff=1,
                    avail_strict=0, usgs_zone=0)
        location = GeoLocation(phytoregion='25E', phytoregion_full='Western High Plains (Omernik)',
                               locality='Grand Staircase Escalante National Monument',
                               geog_area='Big Cottonwood Canyon',
                               directions=('Head NE on HWY 62/180 for 30 miles and turn left on '
                                        'county road 243. Continue on 243 for 8.3 miles then turn '
                                        'left onto county toad 126A. Continue on 126A for 12 miles '
                                        'then turn right. Continue for approximately 1.1 miles to '
                                        'reach collection site.'),
                               degrees_n=38, minutes_n=20, seconds_n=16.32, degrees_w=107, minutes_w=53,
                               seconds_w=59.64, latitude_decimal=38.33786, longitude_decimal=-107.8999,
                               georef_source='GPS', gps_datum='NAD83', altitude=7100, altitude_unit='ft',
                               altitude_in_m=2164, fo_name='UNCOMPAHGRE FIELD OFFICE',
                               district_name='SOUTHWEST DISTRICT OFFICE', state='CO', county='Montrose',
                               location_description=desc, zone=zone)
        accession = Accession(data_source='UP', plant_habit='Forb/herb',
                              coll_date=datetime.date(year=2004, month=8, day=24), acc_num='UP-76',
                              acc_num1='UP', acc_num2='76', acc_num3=None,
                              collected_with='GVR, CH, SP',
                              collection_misc=('Hand-pick ripe seeds, all stages still on plants.'
                                               'This Aster glaucodes is in a nice loamy field (not rocky cliff '
                                               'like other Aster glaucodes)'), seed_source='P',
                              description='Height: 0.15-0.45 m',
                              notes=('Official SOS collection number is NM930N-69: details '
                                     'submitted to SOS National Office by Farmington BLM Botanist.  '
                                     'Germination and competition trials for early seral species '
                                     '(Chicago Botanic Garden).  Photos of habitat, plant and seed'),
                              increase=0, species=plant, location=location)
        db.session.add(plant)
        db.session.add(desc)
        db.session.add(zone)
        db.session.add(location)
        db.session.add(accession)
        db.session.commit()

    def test_accession_species_relationship(self):
        plant = Species(symbol='ABAB', name_full='Abutilon abutiloides', common='shrubby Indian mallow',
                        family='Malvaceae', genus='Abutilon', species='abutiloides', var_ssp1=None, var_ssp2=None,
                        plant_type=None, plant_duration=None, priority_species=0, gsg_val=0,
                        poll_val=0, research_val=0)
        desc = GeoLocationDescription(land_owner='BLM',
                                      associated_taxa_full=('Quercus gambelii:'
                                                         'Ericameria nauseosa ssp. consimilis var. '
                                                         'nitida:Artemisia tridentata ssp. '
                                                         'wyomingensis:Lepidium sp.:Rosa woodsii:'
                                                         'Heterotheca villosa var. villosa:Carex '
                                                         'geyeri:Koeleria macrantha'),
                                      mod='grazed, trampled', mod2='recreation', geomorphology=None,
                                      slope='5-25 degrees', aspect='varied',
                                      habitat='Mountain Brush; meadow along road',
                                      geology='Quaternary, alluvial deposits',
                                      soil_type='Asphalt and sand, tan/red',
                                      population_size=200, occupancy=1500)
        zone = Zone(ptz='10 - 15 Deg. F./6 - 12', us_l4_code='20c',
                    us_l4_name='Semiarid Benchlands and Canyonlands',
                    us_l3_code='20', us_l3_name='Colorado Plateaus',
                    achy_sz_gridcode=11, achy_sz_zone='L1L2H3', cp_buff=1, cp_strict=1, avail_buff=1,
                    avail_strict=0, usgs_zone=0)
        location = GeoLocation(phytoregion='25E', phytoregion_full='Western High Plains (Omernik)',
                               locality='Grand Staircase Escalante National Monument',
                               geog_area='Big Cottonwood Canyon',
                               directions=('Head NE on HWY 62/180 for 30 miles and turn left on '
                                        'county road 243. Continue on 243 for 8.3 miles then turn '
                                        'left onto county toad 126A. Continue on 126A for 12 miles '
                                        'then turn right. Continue for approximately 1.1 miles to '
                                        'reach collection site.'),
                               degrees_n=38, minutes_n=20, seconds_n=16.32, degrees_w=107, minutes_w=53,
                               seconds_w=59.64, latitude_decimal=38.33786, longitude_decimal=-107.8999,
                               georef_source='GPS', gps_datum='NAD83', altitude=7100, altitude_unit='ft',
                               altitude_in_m=2164, fo_name='UNCOMPAHGRE FIELD OFFICE',
                               district_name='SOUTHWEST DISTRICT OFFICE', state='CO', county='Montrose',
                               location_description=desc, zone=zone)
        accession = Accession(data_source='UP', plant_habit='Forb/herb',
                              coll_date=datetime.date(year=2004, month=8, day=24), acc_num='UP-76',
                              acc_num1='UP', acc_num2='76', acc_num3=None,
                              collected_with='GVR, CH, SP',
                              collection_misc=('Hand-pick ripe seeds, all stages still on plants.'
                                               'This Aster glaucodes is in a nice loamy field (not rocky cliff '
                                               'like other Aster glaucodes)'), seed_source='P',
                              description='Height: 0.15-0.45 m',
                              notes=('Official SOS collection number is NM930N-69: details '
                                     'submitted to SOS National Office by Farmington BLM Botanist.  '
                                     'Germination and competition trials for early seral species '
                                     '(Chicago Botanic Garden).  Photos of habitat, plant and seed'),
                              increase=0, species=plant, location=location)
        db.session.add(plant)
        db.session.add(desc)
        db.session.add(zone)
        db.session.add(location)
        db.session.add(accession)
        db.session.commit()
        self.assertIn(accession, plant.accessions.all())
        self.assertEqual(accession.species, plant)

    def test_testing_accession_relationship(self):
        plant = Species(symbol='ABAB', name_full='Abutilon abutiloides', common='shrubby Indian mallow',
                        family='Malvaceae', genus='Abutilon', species='abutiloides', var_ssp1=None, var_ssp2=None,
                        plant_type=None, plant_duration=None, priority_species=0, gsg_val=0,
                        poll_val=0, research_val=0)
        desc = GeoLocationDescription(land_owner='BLM',
                                      associated_taxa_full=('Quercus gambelii:'
                                                         'Ericameria nauseosa ssp. consimilis var. '
                                                         'nitida:Artemisia tridentata ssp. '
                                                         'wyomingensis:Lepidium sp.:Rosa woodsii:'
                                                         'Heterotheca villosa var. villosa:Carex '
                                                         'geyeri:Koeleria macrantha'),
                                      mod='grazed, trampled', mod2='recreation', geomorphology=None,
                                      slope='5-25 degrees', aspect='varied',
                                      habitat='Mountain Brush; meadow along road',
                                      geology='Quaternary, alluvial deposits',
                                      soil_type='Asphalt and sand, tan/red',
                                      population_size=200, occupancy=1500)
        zone = Zone(ptz='10 - 15 Deg. F./6 - 12', us_l4_code='20c',
                    us_l4_name='Semiarid Benchlands and Canyonlands',
                    us_l3_code='20', us_l3_name='Colorado Plateaus',
                    achy_sz_gridcode=11, achy_sz_zone='L1L2H3', cp_buff=1, cp_strict=1, avail_buff=1,
                    avail_strict=0, usgs_zone=0)
        location = GeoLocation(phytoregion='25E', phytoregion_full='Western High Plains (Omernik)',
                               locality='Grand Staircase Escalante National Monument',
                               geog_area='Big Cottonwood Canyon',
                               directions=('Head NE on HWY 62/180 for 30 miles and turn left on '
                                        'county road 243. Continue on 243 for 8.3 miles then turn '
                                        'left onto county toad 126A. Continue on 126A for 12 miles '
                                        'then turn right. Continue for approximately 1.1 miles to '
                                        'reach collection site.'),
                               degrees_n=38, minutes_n=20, seconds_n=16.32, degrees_w=107, minutes_w=53,
                               seconds_w=59.64, latitude_decimal=38.33786, longitude_decimal=-107.8999,
                               georef_source='GPS', gps_datum='NAD83', altitude=7100, altitude_unit='ft',
                               altitude_in_m=2164, fo_name='UNCOMPAHGRE FIELD OFFICE',
                               district_name='SOUTHWEST DISTRICT OFFICE', state='CO', county='Montrose',
                               location_description=desc, zone=zone)
        accession = Accession(data_source='UP', plant_habit='Forb/herb',
                              coll_date=datetime.date(year=2004, month=8, day=24), acc_num='UP-76',
                              acc_num1='UP', acc_num2='76', acc_num3=None,
                              collected_with='GVR, CH, SP',
                              collection_misc=('Hand-pick ripe seeds, all stages still on plants.'
                                               'This Aster glaucodes is in a nice loamy field (not rocky cliff '
                                               'like other Aster glaucodes)'), seed_source='P',
                              description='Height: 0.15-0.45 m',
                              notes=('Official SOS collection number is NM930N-69: details '
                                     'submitted to SOS National Office by Farmington BLM Botanist.  '
                                     'Germination and competition trials for early seral species '
                                     '(Chicago Botanic Garden).  Photos of habitat, plant and seed'),
                              increase=0, species=plant, location=location)
        test = Testing(amt_rcvd_lbs=0.7829348, clean_wt_lbs=0.523494, est_seed_lb=351627,
                       est_pls_lb=297054.4896, est_pls_collected=5346.980813, test_type='XPC',
                       test_date=datetime.date(2003, 3, 12), purity=98, tz=60, fill=90, accession=accession)
        db.session.add(plant)
        db.session.add(desc)
        db.session.add(zone)
        db.session.add(location)
        db.session.add(accession)
        db.session.add(test)
        db.session.commit()
        self.assertEqual(accession, test.accession)
        self.assertIn(test, accession.tests)

    def test_availability_accession_relationship(self):
        plant = Species(symbol='ABAB', name_full='Abutilon abutiloides', common='shrubby Indian mallow',
                        family='Malvaceae', genus='Abutilon', species='abutiloides', var_ssp1=None, var_ssp2=None,
                        plant_type=None, plant_duration=None, priority_species=0, gsg_val=0,
                        poll_val=0, research_val=0)
        desc = GeoLocationDescription(land_owner='BLM',
                                      associated_taxa_full=('Quercus gambelii:'
                                                         'Ericameria nauseosa ssp. consimilis var. '
                                                         'nitida:Artemisia tridentata ssp. '
                                                         'wyomingensis:Lepidium sp.:Rosa woodsii:'
                                                         'Heterotheca villosa var. villosa:Carex '
                                                         'geyeri:Koeleria macrantha'),
                                      mod='grazed, trampled', mod2='recreation', geomorphology=None,
                                      slope='5-25 degrees', aspect='varied',
                                      habitat='Mountain Brush; meadow along road',
                                      geology='Quaternary, alluvial deposits',
                                      soil_type='Asphalt and sand, tan/red',
                                      population_size=200, occupancy=1500)
        zone = Zone(ptz='10 - 15 Deg. F./6 - 12', us_l4_code='20c',
                    us_l4_name='Semiarid Benchlands and Canyonlands',
                    us_l3_code='20', us_l3_name='Colorado Plateaus',
                    achy_sz_gridcode=11, achy_sz_zone='L1L2H3', cp_buff=1, cp_strict=1, avail_buff=1,
                    avail_strict=0, usgs_zone=0)
        location = GeoLocation(phytoregion='25E', phytoregion_full='Western High Plains (Omernik)',
                               locality='Grand Staircase Escalante National Monument',
                               geog_area='Big Cottonwood Canyon',
                               directions=('Head NE on HWY 62/180 for 30 miles and turn left on '
                                        'county road 243. Continue on 243 for 8.3 miles then turn '
                                        'left onto county toad 126A. Continue on 126A for 12 miles '
                                        'then turn right. Continue for approximately 1.1 miles to '
                                        'reach collection site.'),
                               degrees_n=38, minutes_n=20, seconds_n=16.32, degrees_w=107, minutes_w=53,
                               seconds_w=59.64, latitude_decimal=38.33786, longitude_decimal=-107.8999,
                               georef_source='GPS', gps_datum='NAD83', altitude=7100, altitude_unit='ft',
                               altitude_in_m=2164, fo_name='UNCOMPAHGRE FIELD OFFICE',
                               district_name='SOUTHWEST DISTRICT OFFICE', state='CO', county='Montrose',
                               location_description=desc, zone=zone)
        accession = Accession(data_source='UP', plant_habit='Forb/herb',
                              coll_date=datetime.date(year=2004, month=8, day=24), acc_num='UP-76',
                              acc_num1='UP', acc_num2='76', acc_num3=None,
                              collected_with='GVR, CH, SP',
                              collection_misc=('Hand-pick ripe seeds, all stages still on plants.'
                                               'This Aster glaucodes is in a nice loamy field (not rocky cliff '
                                               'like other Aster glaucodes)'), seed_source='P',
                              description='Height: 0.15-0.45 m',
                              notes=('Official SOS collection number is NM930N-69: details '
                                     'submitted to SOS National Office by Farmington BLM Botanist.  '
                                     'Germination and competition trials for early seral species '
                                     '(Chicago Botanic Garden).  Photos of habitat, plant and seed'),
                              increase=0, species=plant, location=location)
        avail = Availability(grin_avail=1.47, bend_avail=17.690088, cbg_avail=0, meeker_avail=0,
                             misc_avail=0, ephraim_avail=0, nau_avail=0.512592, accession=accession,
                             misc_avail_inst=None)
        db.session.add(plant)
        db.session.add(desc)
        db.session.add(zone)
        db.session.add(location)
        db.session.add(accession)
        db.session.add(avail)
        db.session.commit()
        self.assertTrue(avail.avail_any)
        self.assertEqual(avail.gr_avail, (1.47 + 17.690088 + 0.512592))
        self.assertEqual(avail.lb_avail, ((1.47 + 17.690088 + 0.512592) * 0.00220462))
        self.assertEqual(avail.sum_gr_no_grin, 17.690088 + 0.512592)
        self.assertTrue(avail.avail_no_grin, True)
        self.assertEqual(avail.sum_lb_no_grin, ((17.690088 + 0.512592) * 0.00220462))
        self.assertEqual(accession, avail.accession)
        self.assertEqual(avail, accession.availability)

    def test_availability_institution_relationship(self):
        plant = Species(symbol='ABAB', name_full='Abutilon abutiloides', common='shrubby Indian mallow',
                        family='Malvaceae', genus='Abutilon', species='abutiloides', var_ssp1=None, var_ssp2=None,
                        plant_type=None, plant_duration=None, priority_species=0, gsg_val=0,
                        poll_val=0, research_val=0)
        desc = GeoLocationDescription(land_owner='BLM',
                                      associated_taxa_full=('Quercus gambelii:'
                                                         'Ericameria nauseosa ssp. consimilis var. '
                                                         'nitida:Artemisia tridentata ssp. '
                                                         'wyomingensis:Lepidium sp.:Rosa woodsii:'
                                                         'Heterotheca villosa var. villosa:Carex '
                                                         'geyeri:Koeleria macrantha'),
                                      mod='grazed, trampled', mod2='recreation', geomorphology=None,
                                      slope='5-25 degrees', aspect='varied',
                                      habitat='Mountain Brush; meadow along road',
                                      geology='Quaternary, alluvial deposits',
                                      soil_type='Asphalt and sand, tan/red',
                                      population_size=200, occupancy=1500)
        zone = Zone(ptz='10 - 15 Deg. F./6 - 12', us_l4_code='20c',
                    us_l4_name='Semiarid Benchlands and Canyonlands',
                    us_l3_code='20', us_l3_name='Colorado Plateaus',
                    achy_sz_gridcode=11, achy_sz_zone='L1L2H3', cp_buff=1, cp_strict=1, avail_buff=1,
                    avail_strict=0, usgs_zone=0)
        location = GeoLocation(phytoregion='25E', phytoregion_full='Western High Plains (Omernik)',
                               locality='Grand Staircase Escalante National Monument',
                               geog_area='Big Cottonwood Canyon',
                               directions=('Head NE on HWY 62/180 for 30 miles and turn left on '
                                        'county road 243. Continue on 243 for 8.3 miles then turn '
                                        'left onto county toad 126A. Continue on 126A for 12 miles '
                                        'then turn right. Continue for approximately 1.1 miles to '
                                        'reach collection site.'),
                               degrees_n=38, minutes_n=20, seconds_n=16.32, degrees_w=107, minutes_w=53,
                               seconds_w=59.64, latitude_decimal=38.33786, longitude_decimal=-107.8999,
                               georef_source='GPS', gps_datum='NAD83', altitude=7100, altitude_unit='ft',
                               altitude_in_m=2164, fo_name='UNCOMPAHGRE FIELD OFFICE',
                               district_name='SOUTHWEST DISTRICT OFFICE', state='CO', county='Montrose',
                               location_description=desc, zone=zone)
        accession = Accession(data_source='UP', plant_habit='Forb/herb',
                              coll_date=datetime.date(year=2004, month=8, day=24), acc_num='UP-76',
                              acc_num1='UP', acc_num2='76', acc_num3=None,
                              collected_with='GVR, CH, SP',
                              collection_misc=('Hand-pick ripe seeds, all stages still on plants.'
                                               'This Aster glaucodes is in a nice loamy field (not rocky cliff '
                                               'like other Aster glaucodes)'), seed_source='P',
                              description='Height: 0.15-0.45 m',
                              notes=('Official SOS collection number is NM930N-69: details '
                                     'submitted to SOS National Office by Farmington BLM Botanist.  '
                                     'Germination and competition trials for early seral species '
                                     '(Chicago Botanic Garden).  Photos of habitat, plant and seed'),
                              increase=0, species=plant, location=location)
        institute1 = Entity(name='Four Corners School of Outdoor Education',
                            address='P.O. Box 1029\n1117 N. Main Street\nMonticello, UT 84535',
                            contact_name='Mark Grover', contact_phone=4355872156,
                            contact_phone_ext=1024, contact_email='mgrover@fourcornersschol.org',
                            request_costs='No')
        avail = Availability(grin_avail=1.47, bend_avail=17.690088, cbg_avail=0, meeker_avail=0,
                             misc_avail=0, ephraim_avail=0, nau_avail=0.512592, accession=accession,
                             misc_avail_inst=institute1)
        db.session.add(plant)
        db.session.add(desc)
        db.session.add(zone)
        db.session.add(location)
        db.session.add(accession)
        db.session.add(institute1)
        db.session.add(avail)
        db.session.commit()
        self.assertEqual(institute1, avail.misc_avail_inst)
        self.assertIn(avail, institute1.availability)

    def test_use_creation(self):
        plant = Species(symbol='ABAB', name_full='Abutilon abutiloides', common='shrubby Indian mallow',
                        family='Malvaceae', genus='Abutilon', species='abutiloides', var_ssp1=None, var_ssp2=None,
                        plant_type=None, plant_duration=None, priority_species=0, gsg_val=0,
                        poll_val=0, research_val=0)
        desc = GeoLocationDescription(land_owner='BLM',
                                      associated_taxa_full=('Quercus gambelii:'
                                                         'Ericameria nauseosa ssp. consimilis var. '
                                                         'nitida:Artemisia tridentata ssp. '
                                                         'wyomingensis:Lepidium sp.:Rosa woodsii:'
                                                         'Heterotheca villosa var. villosa:Carex '
                                                         'geyeri:Koeleria macrantha'),
                                      mod='grazed, trampled', mod2='recreation', geomorphology=None,
                                      slope='5-25 degrees', aspect='varied',
                                      habitat='Mountain Brush; meadow along road',
                                      geology='Quaternary, alluvial deposits',
                                      soil_type='Asphalt and sand, tan/red',
                                      population_size=200, occupancy=1500)
        zone = Zone(ptz='10 - 15 Deg. F./6 - 12', us_l4_code='20c',
                    us_l4_name='Semiarid Benchlands and Canyonlands',
                    us_l3_code='20', us_l3_name='Colorado Plateaus',
                    achy_sz_gridcode=11, achy_sz_zone='L1L2H3', cp_buff=1, cp_strict=1, avail_buff=1,
                    avail_strict=0, usgs_zone=0)
        location = GeoLocation(phytoregion='25E', phytoregion_full='Western High Plains (Omernik)',
                               locality='Grand Staircase Escalante National Monument',
                               geog_area='Big Cottonwood Canyon',
                               directions=('Head NE on HWY 62/180 for 30 miles and turn left on '
                                        'county road 243. Continue on 243 for 8.3 miles then turn '
                                        'left onto county toad 126A. Continue on 126A for 12 miles '
                                        'then turn right. Continue for approximately 1.1 miles to '
                                        'reach collection site.'),
                               degrees_n=38, minutes_n=20, seconds_n=16.32, degrees_w=107, minutes_w=53,
                               seconds_w=59.64, latitude_decimal=38.33786, longitude_decimal=-107.8999,
                               georef_source='GPS', gps_datum='NAD83', altitude=7100, altitude_unit='ft',
                               altitude_in_m=2164, fo_name='UNCOMPAHGRE FIELD OFFICE',
                               district_name='SOUTHWEST DISTRICT OFFICE', state='CO', county='Montrose',
                               location_description=desc, zone=zone)
        accession = Accession(data_source='UP', plant_habit='Forb/herb',
                              coll_date=datetime.date(year=2004, month=8, day=24), acc_num='UP-76',
                              acc_num1='UP', acc_num2='76', acc_num3=None,
                              collected_with='GVR, CH, SP',
                              collection_misc=('Hand-pick ripe seeds, all stages still on plants.'
                                               'This Aster glaucodes is in a nice loamy field (not rocky cliff '
                                               'like other Aster glaucodes)'), seed_source='P',
                              description='Height: 0.15-0.45 m',
                              notes=('Official SOS collection number is NM930N-69: details '
                                     'submitted to SOS National Office by Farmington BLM Botanist.  '
                                     'Germination and competition trials for early seral species '
                                     '(Chicago Botanic Garden).  Photos of habitat, plant and seed'),
                              increase=0, species=plant, location=location)
        use = AmountUsed(amount_gr=3.431, purpose=("We’re planning to set up a field study that is a "
                                            "combination common garden and diversity trial (are "
                                            "there differences in functional traits between "
                                            "populations AND do we get a boost in productivity/seed "
                                            "production/etc when plants from different populations "
                                            "(of the same species) are grown together."),
                         date_start=datetime.date(2017, 9, 1), date_end=None,
                         start_notes=("I'm also interested in tackling the question Scott Jensen raised of "
                               "incorporating Colorado Plateau accessions in their Great Basin "
                               "production beds to produce diverse seed that can be used throughout "
                               "a provisional seed zone. I worked with the species they're thinking "
                               "of trying this with (Penstemon pachyphyllus) for my dissertation, and "
                               "found significant outbreeding depression during the first generation "
                               "when I artificially crossed populations between the Great Basin and "
                               "Colorado Plateau ecoregions. I of course haven't published this stuff, "
                               "but have talked with Scott about it. I’ve published everything else I "
                               "did on the species (molecular and common garden research, but not the "
                               "outbreeding stuff – I’m attaching very brief summary slides here, and "
                               "my thesis is also available to download through the GBNPP website if "
                               "anyone wants the nitty gritty details). The potential for outbreeding "
                               "depression to have strong and lasting impacts on seed produced is "
                               "clearly something that needs to be sorted as the GB develops material "
                               "for species that occur in the CP. Other species that Scott mentioned "
                               "where I think we can help tackle this question include Heliomeris "
                               "(but again the ssp issues comes up), Machaeranthera canescens, and "
                               "Linum lewisii, which is a key reason we’re focusing on them now."),
                         end_notes=None, accession=accession, species=plant)
        db.session.add(plant)
        db.session.add(desc)
        db.session.add(zone)
        db.session.add(location)
        db.session.add(accession)
        db.session.add(use)
        db.session.commit()
        self.assertEqual(use.amount_lb, (3.431 * 0.00220462))
        self.assertIn(use, plant.uses)
        self.assertIn(use, accession.uses)
        self.assertEqual(plant, use.species)
        self.assertEqual(accession, use.accession)

    def test_release_creation(self):
        plant = Species(symbol='ABAB', name_full='Abutilon abutiloides', common='shrubby Indian mallow',
                        family='Malvaceae', genus='Abutilon', species='abutiloides', var_ssp1=None, var_ssp2=None,
                        plant_type=None, plant_duration=None, priority_species=0, gsg_val=0,
                        poll_val=0, research_val=0)
        desc = GeoLocationDescription(land_owner='BLM',
                                      associated_taxa_full=('Quercus gambelii:'
                                                         'Ericameria nauseosa ssp. consimilis var. '
                                                         'nitida:Artemisia tridentata ssp. '
                                                         'wyomingensis:Lepidium sp.:Rosa woodsii:'
                                                         'Heterotheca villosa var. villosa:Carex '
                                                         'geyeri:Koeleria macrantha'),
                                      mod='grazed, trampled', mod2='recreation', geomorphology=None,
                                      slope='5-25 degrees', aspect='varied',
                                      habitat='Mountain Brush; meadow along road',
                                      geology='Quaternary, alluvial deposits',
                                      soil_type='Asphalt and sand, tan/red',
                                      population_size=200, occupancy=1500)
        zone = Zone(ptz='10 - 15 Deg. F./6 - 12', us_l4_code='20c',
                    us_l4_name='Semiarid Benchlands and Canyonlands',
                    us_l3_code='20', us_l3_name='Colorado Plateaus',
                    achy_sz_gridcode=11, achy_sz_zone='L1L2H3', cp_buff=1, cp_strict=1, avail_buff=1,
                    avail_strict=0, usgs_zone=0)
        location = GeoLocation(phytoregion='25E', phytoregion_full='Western High Plains (Omernik)',
                               locality='Grand Staircase Escalante National Monument',
                               geog_area='Big Cottonwood Canyon',
                               directions=('Head NE on HWY 62/180 for 30 miles and turn left on '
                                        'county road 243. Continue on 243 for 8.3 miles then turn '
                                        'left onto county toad 126A. Continue on 126A for 12 miles '
                                        'then turn right. Continue for approximately 1.1 miles to '
                                        'reach collection site.'),
                               degrees_n=38, minutes_n=20, seconds_n=16.32, degrees_w=107, minutes_w=53,
                               seconds_w=59.64, latitude_decimal=38.33786, longitude_decimal=-107.8999,
                               georef_source='GPS', gps_datum='NAD83', altitude=7100, altitude_unit='ft',
                               altitude_in_m=2164, fo_name='UNCOMPAHGRE FIELD OFFICE',
                               district_name='SOUTHWEST DISTRICT OFFICE', state='CO', county='Montrose',
                               location_description=desc, zone=zone)
        accession = Accession(data_source='UP', plant_habit='Forb/herb',
                              coll_date=datetime.date(year=2004, month=8, day=24), acc_num='UP-76',
                              acc_num1='UP', acc_num2='76', acc_num3=None,
                              collected_with='GVR, CH, SP',
                              collection_misc=('Hand-pick ripe seeds, all stages still on plants.'
                                               'This Aster glaucodes is in a nice loamy field (not rocky cliff '
                                               'like other Aster glaucodes)'), seed_source='P',
                              description='Height: 0.15-0.45 m',
                              notes=('Official SOS collection number is NM930N-69: details '
                                     'submitted to SOS National Office by Farmington BLM Botanist.  '
                                     'Germination and competition trials for early seral species '
                                     '(Chicago Botanic Garden).  Photos of habitat, plant and seed'),
                              increase=0, species=plant, location=location)
        rel = Release(loc_desc='Western Colorado', germ_origin='NRCS', name="'Paloma'", year=1974,
                      release_type='cultivar', plant_origin='native',
                      used_for='soil stabilization and range revegetation',
                      select_criteria='establishment, vigor, and forage production in dry land',
                      special_character='superior seed and forage production',
                      adaptation='Western US', prime_pmc='NMPMC', primary_releasing='NMPMC',
                      secondary_releasing='AZAES, COAES, NMAES', cp_adapted=1, cp_sourced=0,
                      source_num='single source', lb_acre_sow=2.4, lb_acre_yield=200,
                      soil_adap='sandy soil', precip_adap='9-10', evel_adap='3000-7500',
                      release_brochure=('https://www.nrcs.usda.gov/Internet/FSE_PLANTMATERIALS/publica'
                                        'tions/nmpmcrb12138.pdf'),
                      comments=('Steve Parr - collected in NW NM - Rio Arriba county - really good '
                                'product'),
                      accession=accession, species=plant)
        db.session.add(plant)
        db.session.add(desc)
        db.session.add(zone)
        db.session.add(location)
        db.session.add(accession)
        db.session.add(rel)
        db.session.commit()
        self.assertIn(rel, plant.releases)
        self.assertIn(rel, accession.releases)
        self.assertEqual(plant, rel.species)
        self.assertEqual(accession, rel.accession)

if __name__ == '__main__':
    create_app().app_context().push()
    unittest.main()
