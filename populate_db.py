import pandas as pd
from sqlalchemy.exc import IntegrityError

from app import app
from models import db, Availability, Species, Accession, Location, LocationDescription, Testing, Zone

df = pd.read_excel('complete_plants_checklist_usda.xlsx')
db_df = pd.read_excel('DB_export_updated123016_noGRINavail_with_SWSP_data.xlsx')


def parse_excel(df):
    for index, row in df.iterrows():
        zone, desc, loc = get_zone_desc_loc(row)
        species, acc = get_species_acc(row)

        if add_acc_to_db(zone, desc, loc, species, acc):
            test = get_test(row, acc)
            add_test_to_db(test)


def add_synonyms(df):
    for index, row in df.iterrows():  # Check if row has synonyms
        check_synonym(row)


def add_species(df):
    for index, row in df.iterrows():
        get_plant(row)


# TODO
"""
Adding those singular model objects to the database could be refactored to be a little more DRY compliant.
"""


def add_acc_to_db(zone, location_description, location, species, accession):
    db.session.add(zone)
    db.session.add(location_description)
    db.session.add(location)
    db.session.add(species)
    db.session.add(accession)
    try:
        db.session.commit()
        print('Successfully added {} to database!'.format(accession.acc_num))
        return True
    except IntegrityError:
        db.session.rollback()
        print('[!] {} already exists in the database!'.format(accession.acc_num))
        return False


def add_plant_to_db(plant):
    db.session.add(plant)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        print('{} already exists in the database!'.format(plant.name_full))


def add_test_to_db(test):
    db.session.add(test)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        print('{} already exists in the database!'.format(test.name_full))


def convert_dd_dms(dd):
    degrees = int(dd)
    minute_dec = (dd - degrees) * 60
    minutes = int(minute_dec)
    seconds = (minute_dec - minutes) * 60

    return degrees, minutes, seconds


def get_species_acc(series):
    data_source = series['DATA_SOURCE']
    plant_habit = series['Habit_rev']
    coll_date = series['COLL_DT']  # Sqlite expects YYYY-MM-DD format
    acc_num = series['ACC_NUM']
    acc_num1 = series['ACC_NUM_1']
    acc_num2 = series['ACC_NUM_2']
    acc_num3 = series['ACC_NUM_3']
    collected_with = series['COLLECTED_WITH']
    collection_misc = series['COLLECTION_MISC']
    seed_source = series['SEED_SOURCE']
    description = series['DESCRIPTION']
    notes = series['notes']
    increase = None  # Slated for increase?

    species = get_species(series['NAME'])
    location = get_zone_desc_loc(series)

    acc = Accession(data_source=data_source, plant_habit=plant_habit, coll_date=coll_date, acc_num=acc_num,
                    acc_num1=acc_num1, acc_num2=acc_num2, acc_num3=acc_num3, collected_with=collected_with,
                    collection_misc=collection_misc, seed_source=seed_source, description=description, notes=notes,
                    increase=increase, species=species, location=location)

    return species, acc


def get_test(series, accession):
    amt_rcvd_lbs = series['AMOUNT_RECVD__LBS_']
    clean_wt_lbs = series['CLEAN_WEIGHT__LBS_']
    est_seed_lb = series['SEED_LB']  # Estimated seeds per pound
    est_pls_lb = series['EST_PLS_LB']  # Estimated Pure Live Seed per pound
    est_pls_collected = series['EST_PLS_COLLECTED']
    test_type = series['TEST_TYPE']
    test_date = series['TEST_DATE']
    purity = series['PURITY_']
    tz = series['TZ_']
    fill = series['FILL_']

    test = Testing(amt_rcvd_lbs=amt_rcvd_lbs, clean_wt_lbs=clean_wt_lbs, est_seed_lb=est_seed_lb, est_pls_lb=est_pls_lb,
                   est_pls_collected=est_pls_collected, test_type=test_type, test_date=test_date, purity=purity, tz=tz,
                   fill=fill, accession=accession)
    return test


def get_zone_desc_loc(series):
    phytoregion = series['PHYTOREGION']
    phytoregion_full = series['PHYTOREGION_FULL']
    locality = series['SUB_CNT3']
    geog_area = series['GEOG_AREA']
    directions = series['LOCALITY']
    latitude_decimal = series['LATITUDE_DECIMAL']
    longitude_decimal = series['LONGITUDE_DECIMAL']
    degrees_n, minutes_n, seconds_n = convert_dd_dms(latitude_decimal)
    degrees_w, minutes_w, seconds_w = convert_dd_dms(longitude_decimal)
    georef_source = series['GEOREF_SOURCE']
    gps_datum = series['GPS_DATUM']
    altitude = series['ALTITUDE']
    altitude_unit = series['ALTITUDE_UNIT']
    altitude_in_m = series['ALTITUDE_IN_M']
    fo_name = series['ADMU_NAME']
    district_name = series['PARENT_NAM']
    state = series['ADMIN_ST']
    county = series['SUB_CNT2']

    zone = get_zone(series)
    location_description = get_location_desc(series)

    loc = Location(phytoregion=phytoregion, phytoregion_full=phytoregion_full, locality=locality, geog_area=geog_area,
                   directions=directions, latitude_decimal=latitude_decimal, longitude_decimal=longitude_decimal,
                   degrees_n=degrees_n, minutes_n=minutes_n, seconds_n=seconds_n, degrees_w=degrees_w,
                   minutes_w=minutes_w, seconds_w=seconds_w, georef_source=georef_source, gps_datum=gps_datum,
                   altitude=altitude, altitude_unit=altitude_unit, altitude_in_m=altitude_in_m, fo_name=fo_name,
                   district_name=district_name, state=state, county=county, zone=zone,
                   location_description=location_description)

    return zone, location_description, loc


def get_location_desc(series):
    land_owner = series['LAND_OWNER']
    associated_taxa_full = series['ASSOCIATED_TAXA_FULL']
    mod = series['USER2']   # modifying factors of collection site (grazed, etc.)
    mod2 = series['USER1']  # additional modifying factors of collection site (roadside, etc.)
    geomorphology = series['GEOMORPHOLOGY']
    slope = series['SLOPE']
    aspect = series['ASPECT']
    habitat = series['HABITAT']
    geology = series['GEOLOGY']
    soil_type = series['SOIL_TYPE']
    population_size = series['POPULATION_SIZE']
    occupancy = series['OCCUPANCY']  # Number of plants collected from

    loc_desc = LocationDescription(land_owner=land_owner, associated_taxa_full=associated_taxa_full, mod=mod, mod2=mod2,
                                   geomorphology=geomorphology, slope=slope, aspect=aspect, habitat=habitat,
                                   geology=geology, soil_type=soil_type, population_size=population_size,
                                   occupancy=occupancy)
    return loc_desc


def get_species(name):
    return db.session.query(Species).filter_by(name_full=name).first()


def get_zone(series):
    ptz = series['Pot_STZ']
    us_l4_code = series['US_L4CODE']
    us_l4_name = series['US_L4NAME']
    us_l3_code = series['US_L3CODE']
    us_l3_name = series['US_L3NAME']
    achy_sz_gridcode = series['ACHY_SZ_GRIDCODE']
    achy_sz_zone = series['ACHY_SZ_ZONE']
    cp_buff = series['CPBuff']
    cp_strict = series['CPStrict']
    avail_buff = series['AVAIL_BUFF']
    avail_strict = series['AVAIL_STRICT']
    usgs_zone = series['USGS_ZONE']

    zone = Zone(ptz=ptz, us_l4_code=us_l4_code, us_l4_name=us_l4_name, us_l3_code=us_l3_code, us_l3_name=us_l3_name,
                achy_sz_gridcode=achy_sz_gridcode, achy_sz_zone=achy_sz_zone, cp_buff=cp_buff, cp_strict=cp_strict,
                avail_buff=avail_buff, avail_strict=avail_strict, usgs_zone=usgs_zone)
    return zone


def get_plant(series):
    if pd.isnull(series['Synonym Symbol']):
        symbol = series['Symbol']
    else:
        symbol = series['Synonym Symbol']

    if not isinstance(series['Scientific Name with Author'], str):
        return  # Skip row if the name is not a string type

    name = series['Scientific Name with Author'].split(' ')
    if len(name) < 2 or name[1][-1] == '.':
        return  # Skip rows with blank names and those that just describe the genus

    common = None
    if not pd.isnull(series['Common Name']):
        common = series['Common Name']

    var_ssp1 = None
    var_ssp2 = None
    if 'var.' in name:
        index = name.index('var.') + 1
        var_ssp1 = 'var.'
        if index != len(name):  # avoid index out of bounds errors for when var. or spp. at end of string
            var_ssp2 = name[index]
    if 'ssp.' in name:
        index = name.index('ssp.') + 1
        var_ssp1 = 'ssp.'
        if index != len(name):
            var_ssp2 = name[index]

    if var_ssp1 and var_ssp2:
        name_full = name[0] + ' ' + name[1] + ' ' + var_ssp1 + ' ' + var_ssp2
    else:
        name_full = name[0] + ' ' + name[1]

    if pd.isnull(series['Family']):
        last = Species.query.filter_by(symbol=series['Symbol']).first()
        if last is not None:
            family = last.family
        else:
            return
    else:
        family = series['Family']

    plant = Species(symbol=symbol, name_full=name_full, common=common, family=family,
                           genus=name[0], species=name[1], var_ssp1=var_ssp1, var_ssp2=var_ssp2,
                           plant_type=None, plant_duration=None, priority_species=0, gsg_val=0,
                           poll_val=0, research_val=0)
    add_plant_to_db(plant)


def check_synonym(series):
    if pd.isnull(series['Synonym Symbol']):
        return
    else:
        plant = Species.query.filter_by(symbol=series['Symbol']).first()
        current = Species.query.filter_by(symbol=series['Synonym Symbol']).first()
        if plant is not None and current is not None:
            plant.add_synonym(current)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                print('Failed to add {} as synonym of {}'.format(current.name_full, plant.name_full))

if __name__ == '__main__':
    db.init_app(app)
    db.create_all()

    # Already added to local database
    #add_species(df)
    #add_synonyms(df)
