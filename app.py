from flask import Flask, render_template, flash, redirect, url_for
import pandas as pd
from sqlalchemy.exc import IntegrityError, InvalidRequestError

import forms
import models

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cpnpp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()

DEBUG = True
PORT = 8000
HOST = '127.0.0.1'

def add_synonyms(df):
  for index, row in df.iterrows():  # Check if row has synonyms
    check_synonym(row)

def add_species(df):
  for index, row in df.iterrows():
    get_plant(row)

def add_to_db(plant):
  models.db.session.add(plant)
  try:
    models.db.session.commit()
  except IntegrityError:
    models.db.session.rollback()
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
    last = models.Species.query.filter_by(symbol=series['Symbol']).first()
    if last is not None:
      family = last.family
    else:
      return
  else:
    family = series['Family']
  
    
  plant = models.Species(symbol=symbol, name_full=name_full, common=common, family=family,
                    genus=name[0], species=name[1], var_ssp1=var_ssp1, var_ssp2=var_ssp2, 
                    plant_type=None, plant_duration=None, priority_species=0, gsg_val=0, 
                    poll_val=0, research_val=0)
  add_to_db(plant)
  
def check_synonym(series):
  if pd.isnull(series['Synonym Symbol']):
    return
  else:
    plant = models.Species.query.filter_by(symbol=series['Symbol']).first()
    current = models.Species.query.filter_by(symbol=series['Synonym Symbol']).first()
    if plant is not None and current is not None:
        plant.add_synonym(current)
        try:
            models.db.session.commit()
        except IntegrityError:
            models.db.session.rollback()
            print('Failed to add {} as synonym of {}'.format(current.name_full, plant.name_full))


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/shipment', methods=('GET', 'POST'))
def shipment():
  form = forms.ShipmentForm()
  form.origin_institute_id.choices = [
    (inst.id, inst.name) for inst in models.Institution.query.order_by('name')]
  form.destination_institute_id.choices = [
    (inst.id, inst.name) for inst in models.Institution.query.order_by('name')]
  form.accession.choices = [
    (acc.id, acc.acc_num) for acc in models.Accession.query.order_by('acc_num')]
  if form.validate_on_submit():
    flash('Yay, Shipment created!', 'success')
    shipment = models.Shipping(
      ship_date=form.ship_date.data, 
      tracking_num=form.tracking_num.data,
      tracking_num_comp=form.tracking_num_comp.data, 
      amount_gr=form.amount_gr.data, 
      calc_by=form.calc_by.data,
      origin_institute=form.origin_instiute.data, 
      destination_institute=form.destination_institute.data,
      accession=form.accession.data,
    )

if __name__ == '__main__':
  models.db.init_app(app)
  models.db.create_all()
  df = pd.read_excel('complete_plants_checklist_usda.xlsx')
  print('[!] Adding species!')
  add_species(df)
  print('[!] Adding synonyms!')
  add_synonyms(df)
  print('[!] Done adding {} Species!'.format(len(models.Species.query.all())))
  app.run(debug=DEBUG, host=HOST, port=PORT)