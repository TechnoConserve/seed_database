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
        models.db.session.query(models.Species).distinct(models.Species.family).group_by(models.Species.family)]
    form.genus.choices = [
        (species.genus, species.genus) for species in
        models.db.session.query(models.Species).distinct(models.Species.genus).group_by(models.Species.genus)]
    form.species.choices = [
        (species.id, species.name_full) for species in
        models.db.session.query(models.Species).distinct(models.Species.name_full).group_by(models.Species.name_full)]
    if form.validate_on_submit():
        species = models.Species.query.get(form.species.data)
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
            species=species,
            location=loc,
        )
        models.db.session.add(desc)
        models.db.session.add(loc)
        models.db.session.add(acc)
        models.db.session.commit()
        flash('Yay, Accession created!', 'success')
        return redirect('/success')
    return render_template('accessions.html', form=form)


@app.route('/availability', methods=('GET', 'POST'))
def availability():
    form = forms.AvailabilityForm()
    form.accession.choices = [
        (acc.id, acc.acc_num) for acc in models.Accession.query.order_by('acc_num')]
    form.misc_inst_id.choices = [
        (inst.id, inst.name) for inst in models.Institution.query.order_by('name')]
    if form.validate_on_submit():
        acc = models.Accession.query.get(form.accession.data)
        misc_inst = models.Institution.query.get(form.misc_inst_id.data)
        grin = form.grin_avail.data
        bend = form.bend_avail.data
        cbg = form.cbg_avail.data
        meeker = form.meeker_avail.data
        misc = form.misc_avail.data
        ephraim = form.ephraim_avail.data
        nau = form.nau_avail.data
        avail = models.Availability(
            grin_avail=grin,
            bend_avail=bend,
            cbg_avail=cbg,
            meeker_avail=meeker,
            misc_avail=misc,
            ephraim_avail=ephraim,
            nau_avail=nau,
            accession=acc,
            misc_avail_inst=misc_inst,
        )
        models.db.session.add(avail)
        models.db.session.commit()
        flash('Yay, availability added for {}'.format(acc.species.name_full), 'success')
        return redirect('/success')
    return render_template('availability.html', form=form)


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


@app.route('/releases', methods=('GET', 'POST'))
def releases():
    form = forms.ReleaseForm()
    form.species.choices = [
        (species.id, species.name_full) for species in
        models.db.session.query(models.Species).distinct(models.Species.name_full).group_by(models.Species.name_full)]
    form.accession.choices = [
        (acc.id, acc.acc_num) for acc in models.Accession.query.order_by('acc_num')]
    if form.validate_on_submit():
        species = models.Species.query.get(form.species.data)
        acc = models.Accession.query.get(form.accession.data)
        release = models.Release(
            loc_desc=form.loc_desc.data,
            germ_origin=form.germ_origin.data,
            name=form.name.data,
            year=form.year.data,
            release_type=form.release_type.data,
            plant_origin=form.plant_origin.data,
            used_for=form.used_for.data,
            select_criteria=form.select_criteria.data,
            special_character=form.special_character.data,
            adaptation=form.adaptation.data,
            prime_pmc=form.prime_pmc.data,
            primary_releasing=form.primary_releasing.data,
            secondary_releasing=form.secondary_releasing.data,
            cp_adapted=form.cp_adapted.data,
            cp_sourced=form.cp_sourced.data,
            source_num=form.source_num.data,
            lb_acre_sow=form.lb_acre_sow.data,
            lb_acre_yield=form.lb_acre_yield.data,
            soil_adap=form.soil_adap.data,
            precip_adap=form.precip_adap.data,
            elev_adap=form.elev_adap.data,
            release_brochure=form.release_brochure.data,
            comments=form.comments.data,
            accession=acc,
            species=species
        )
        models.db.session.add(release)
        models.db.session.commit()
        flash('Yay, release for {} created!'.format(species.name_full), 'success')
        return redirect('/success')
    return render_template('releases.html', form=form)


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
        origin_institute = models.Institution.query.get(form.origin_institute_id.data)
        destination_institute = models.Institution.query.get(form.destination_institute_id.data)
        accession = models.Accession.query.get(form.accession.data)
        shipment = models.Shipping(
            ship_date=form.ship_date.data,
            tracking_num=form.tracking_num.data,
            tracking_num_comp=form.tracking_num_comp.data,
            amount_gr=form.amount_gr.data,
            calc_by=form.calc_by.data,
            origin_institute=origin_institute,
            destination_institute=destination_institute,
            accession=accession,
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


@app.route('/synonyms', methods=('GET', 'POST'))
def synonyms():
    form = forms.SynonymsForm()
    form.species.choices = [
        (species.id, species.name_full) for species in
        models.db.session.query(models.Species).distinct(models.Species.name_full).group_by(models.Species.name_full)
    ]
    form.synonym.choices = [
        (species.id, species.name_full) for species in
        models.db.session.query(models.Species).distinct(models.Species.name_full).group_by(models.Species.name_full)
    ]
    if form.validate_on_submit():
        plant = models.Species.query.get(form.species.data)
        synonym = models.Species.query.get(form.synonym.data)
        plant.add_synonym(synonym)
        models.db.session.commit()
        flash('Yay, {} successfully added as a synonym of {}'.format(synonym.name_full, plant.name_full), 'success')
        return redirect('/success')
    return render_template('synonyms.html', form=form)


@app.route('/testing', methods=('GET', 'POST'))
def testing():
    form = forms.TestingForm()
    form.accession.choices = [
        (acc.id, acc.acc_num) for acc in models.Accession.query.order_by('acc_num')]
    if form.validate_on_submit():
        accession = models.Accession.query.get(form.accession.data)
        test = models.Testing(
            amt_rcvd_lbs=form.amt_rcvd_lbs.data,
            clean_wt_lbs=form.clean_wt_lbs.data,
            est_seed_lb=form.est_seed_lb.data,
            est_pls_lb=form.est_pls_lb.data,
            est_pls_collected=form.est_pls_collected,
            test_type=form.test_type.data,
            test_date=form.test_date.data,
            purity=form.purity.data,
            tz=form.tz.data,
            fill=form.fill.data,
            accession=accession
        )
        models.db.session.add(test)
        models.db.session.commit()
        flash('Yay, test added for {}'.format(form.accession.data))
        return redirect('/success')
    return render_template('testing.html', form=form)


@app.route('/uses', methods=('GET', 'POST'))
def uses():
    form = forms.UseForm()
    form.accession.choices = [
        (acc.id, acc.acc_num) for acc in models.Accession.query.order_by('acc_num')]
    if form.validate_on_submit():
        accession = models.Accession.query.get(form.accession.data)
        species = accession.species
        use = models.Use(
            amount_gr=form.amount_gr.data,
            purpose=form.purpose.data,
            date_start=form.date_start.data,
            date_end=form.date_end.data,
            start_notes=form.start_notes.data,
            end_notes=form.end_notes.data,
            accession=accession,
            species=species
        )
        models.db.session.add(use)
        models.db.session.commit()
        flash('Yay, Use created for {}.'.format(species.name_full), 'success')
        return redirect('/success')
    return render_template('use.html', form=form)


if __name__ == '__main__':
    models.db.init_app(app)
    models.db.create_all()

    app.run()
