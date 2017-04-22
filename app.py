from flask import Flask, redirect, render_template, flash

import forms
import models

app = Flask(__name__)
app.config.from_pyfile('settings.cfg')
app.app_context().push()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/shipments', methods=('GET', 'POST'))
def shipments():
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
        return redirect('/success')
    return render_template('shipments.html', form=form)


@app.route('/species', methods=('GET', 'POST'))
def species():
    form = forms.SpeciesForm()
    if form.validate_on_submit():
        flash('Yay, Species created!', 'success')
        species = models.Species(
            symbol=form.symbol.data,
            name_full=form.name_full.data,
            common=form.common.data,
            family=form.family.data,
            genus=form.genus.data,
            species=form.species.data,
            var_ssp1=form.var_ssp1.data,
            var_ssp2=form.var_ssp2.data,
            plant_type=form.plant_type.data,
            plant_duration=form.plant_duration
        )
        return redirect('/success')
    return render_template('species.html', form=form)


@app.route('/success')
def success():
    return 'Success!'


if __name__ == '__main__':
    models.db.init_app(app)
    models.db.create_all()

    app.run()
