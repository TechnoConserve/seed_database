import pandas as pd
from sqlalchemy.exc import IntegrityError

from app import app
from models import db, Species

df = pd.read_excel('complete_plants_checklist_usda.xlsx')


def add_synonyms(df):
    for index, row in df.iterrows():  # Check if row has synonyms
        check_synonym(row)


def add_species(df):
    for index, row in df.iterrows():
        get_plant(row)


def add_to_db(plant):
    db.session.add(plant)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        print('{} already exists in the database!'.format(plant.name_full))


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

    last = None
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
    add_to_db(plant)


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
    print('[!] Adding species!')
    add_species(df)
    print('[!] Adding synonyms!')
    add_synonyms(df)
    print('[!] Done adding {} Species!'.format(len(Species.query.all())))