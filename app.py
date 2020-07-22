#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import *


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # TODO: replace with real venues data,
    # num_shows should be aggregated based on number of upcoming shows per venue.
  cities_and_state = Venue.query.distinct(Venue.city, Venue.state).all()
  data = [v.venuesInCity for v in cities_and_state]
  
  return render_template('pages/venues.html', areas=data);


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # search for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
      search_term= request.form.get('search_term', None)
      Venues = Venue.query.filter(Venue.name.ilike('%' + search_term + '%')).all()
      count = len(Venues)
      response = {
        "data" : [ven.venueDetails for ven in Venues],
        "count" : count
      }

      return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venues = Venue.query.filter(Venue.id == venue_id).one_or_none()

  data = venues.venueDetails_UpcomingDetails

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  venue_form = VenueForm(request.form)
  try:
    new_venue = Venue(
            name=venue_form.name.data,
            genres=venue_form.genres.data,
            address=venue_form.address.data,
            city=venue_form.city.data,
            state=venue_form.state.data,
            phone=venue_form.phone.data,
            facebook_link=venue_form.facebook_link.data,
            image_link=venue_form.image_link.data)

    new_venue.add()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  except:
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  # on successful db insert, flash success
  
  
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  venueDelete = Venue.query.filter(venue.id == venue_id)
  venueDelete.delete()
  flask("Venue {0} has been deleted successfully".format(venueDelete[0]['name']))
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  artists = Artist.query.all()
  data=[art.artistDetails_Shows for art in artists]
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term= request.form.get('search_term', None)
  artists = Artist.query.filter(Artist.name.ilike('%' + search_term + '%')).all()
  count = len(artists)
  response={"count": count, "data": [a.artistDetails for a in artists]}
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  artist = Artist.query.filter(Artist.id == artist_id).one()
  data = artist.artistDetails_Shows

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artistUpdate = Artist.query.filter(Artist.id == artist_id).one_or_none()
  artist = artistUpdate.artistDetails
  form = ArtistForm(data=artist)
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  form = ArtistForm(request.form)
  try:
      art = Artist.query.filter_by(id=artist_id)
      art.name = form.name.data,
      art.genres = json.dumps(form.genres.data),
      art.city = form.city.data,
      art.state = form.state.data,
      art.phone = form.phone.data,
      art.facebook_link = form.facebook_link.data,
      art.image_link = form.image_link.data,
      art.update()
  except:
      render_template('errors/404.html')
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venueUpdata = Venue.query.filter(Venue.id == venue_id)

  venue = venueUpdata.venueDetails
  form = VenueForm(data=venue)
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  form = VenueForm(request.form)
  try:
      ven = Venue.query.filter(Venue.id==venue_id).one()
      ven.name = form.name.data,
      ven.address = form.address.data,
      ven.genres = '.'.join(form.genres.data),
      ven.city = form.city.data,
      ven.state = form.state.data,
      ven.phone = form.phone.data,
      ven.facebook_link = form.facebook_link.data,
      ven.image_link = form.image_link.data,
      ven.update()
  except:
      flash('Show Could not be edited')
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  artist_form = ArtistForm(request.form)
  
  try:
    new_artist = Artist(
      name=artist_form.name.data,
      genres=artist_form.genres.data,
      #address=artist_form.address.data,
      city=artist_form.city.data,
      state=artist_form.state.data,
      phone=artist_form.phone.data,
      facebook_link=artist_form.facebook_link.data,
      image_link=artist_form.image_link.data)
    new_artist.add()
    flash('Show was successfully listed!')
  except:
    flash('Show Could not be added')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  Shows = Show.query.all()
  data = [so.showDetails_Artits_Venue for so in Shows]
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  show_form = ShowForm(request.form)
  
  show = Show(
      artist_id=show_form.artist_id.data,
      venue_id=show_form.venue_id.data,
      start_time=show_form.start_time.data
      )
  show.add()
  flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
