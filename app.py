from flask import Flask, redirect, render_template, flash

import forms
import models

app = Flask(__name__)
app.config.from_pyfile('settings.cfg')
app.app_context().push()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/accessions')
def accessions():
    form = forms.AccessionForm()
    form.family.choices = [
        (species.family, species.family) for species in
        models.db.session.query(models.Species).distinct(models.Species.family).group_by(models.Species.family)
    ]
    form.genus.choices = [
        (species.genus, species.genus) for species in
        models.db.session.query(models.Species).distinct(models.Species.genus).group_by(models.Species.genus)
    ]
    form.species.choices = [
        (species.id, species.name_full) for species in
        models.db.session.query(models.Species).distinct(models.Species.name_full).group_by(models.Species.name_full)
    ]
    if form.validate_on_submit():
        # Need to create the LocationDescription object first
        desc = models.LocationDescription(
            land_owner=form.land_owner.data,
            associated_taxa_full=form.associated_taxa_full.data,
            mod=form.mod.data,
            mod2=form.mod2.data,
            geomorphology=form.geomorphology.data,
            slope=form.slope.data,
            aspect=form.aspect.data,
            habitat=form.habitat.data,
            geology=form.geology.data,
            soil_type=form.soil_type.data,
            population_size=form.population_size.data,
            occupancy=form.occupancy.data
        )
        # TODO Compute the data needed to create the Zone object
        # Then we create the Location object
        altitude = form.altitude.data
        unit = form.altitude_unit.data
        if unit == 'm':
            altitude_m = altitude
        else:
            altitude_m = int(altitude * 0.3048)
        loc = models.Location(
            phytoregion=form.phytoregion.data,
            phytoregion_full=form.phytoregion_full.data,
            locality=form.locality.data,
            geog_area=form.geog_area.data,
            directions=form.directions.data,
            degrees_n=form.degrees_n.data,
            minutes_n=form.minutes_n.data,
            seconds_n=form.seconds_n.data,
            degrees_w=form.degrees_w.data,
            minutes_w=form.minutes_w.data,
            seconds_w=form.seconds_w.data,
            latitude_decimal=form.latitute_decimal.data,
            longitude_decimal=form.longitude_decimal.data,
            georef_source=form.georef_source.data,
            gps_datum=form.gps_datum.data,
            altitude=altitude,
            altitude_unit=unit,
            altitude_in_m=altitude_m,
            fo_name=form.fo_name.data,
            district_name=form.district_name.data,
            state=form.state.data,
            county=form.county.data,
            location_description=desc,
            zone=None
        )
        # Finally we create the Accession object
        acc_num = form.acc_num.data
        split = acc_num.split('-')
        acc_num1 = split[0]
        acc_num2 = None
        acc_num3 = None
        if len(split) > 1:
            acc_num2 = split[1]
        if len(split) > 2:
            acc_num3 = split[2]
        acc = models.Accession(
            data_source=form.data_source.data,
            plant_habit=form.plant_habit.data,
            coll_date=form.coll_date.data,
            acc_num=acc_num,
            acc_num1=acc_num1,
            acc_num2=acc_num2,
            acc_num3=acc_num3,
            collected_with=form.collected_with.data,
            collection_misc=form.collection_misc.data,
            seed_source=form.seed_source.data,
            description=form.description.data,
            notes=form.notes.data,
            increase=0,
            species=form.species.data,
            location=loc,
        )
        models.db.session.add(desc)
        models.db.session.add(loc)
        models.db.session.add(acc)
        models.db.session.commit()
        flash('Yay, Accession created!', 'success')
        return redirect('/success')
    return render_template('accessions.html', form=form)


@app.route('/institutions', methods=('GET', 'POST'))
def institutions():
    form = forms.InstitutionForm()
    if form.validate_on_submit():
        institute = models.Institution(
            name=form.name.data,
            address=form.address.data,
            contact_name=form.contact_name.data,
            contact_phone=form.contact_phone.data,
            contact_phone_ext=form.contact_phone_ext.data,
            contact_email=form.contact_email.data,
            request_costs=form.request_costs.data
        )
        models.db.session.add(institute)
        models.db.session.commit()
        flash('Yay, Institution created!', 'success')
        return redirect('/success')
    return render_template('institutions.html', form=form)


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
        models.db.session.add(shipment)
        models.db.session.commit()
        flash('Yay, Shipment created!', 'success')
        return redirect('/success')
    return render_template('shipments.html', form=form)


@app.route('/species', methods=('GET', 'POST'))
def species():
    form = forms.SpeciesForm()
    if form.validate_on_submit():
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
        models.db.session.add(species)
        models.db.session.commit()
        flash('Yay, Species created!', 'success')
        return redirect('/success')
    return render_template('species.html', form=form)


@app.route('/success')
def success():
    return 'Success!'


if __name__ == '__main__':
    models.db.init_app(app)
    models.db.create_all()

    app.run()
