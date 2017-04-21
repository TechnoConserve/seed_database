from flask import Flask, render_template, flash, redirect, url_for
import pandas as pd

import forms
import models

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cpnpp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()

DEBUG = True
PORT = 8000
HOST = '127.0.0.1'


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

  app.run(debug=DEBUG, host=HOST, port=PORT)