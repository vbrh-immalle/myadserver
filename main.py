from flask import Flask, url_for, g, render_template, send_file
from db import Db
import db
import models

app = Flask(__name__)

def get_db():
    if 'db' not in g:
        g.db = Db()
    return g.db

@app.route('/')
def index():
    return render_template('index.html', 
        aantal_resellers = get_db().get_aantal_resellers(),
        aantal_ads = get_db().get_aantal_ads())

@app.route('/ceo')
def ceo():
    lines = get_db().get_ceo_data()
    return render_template('ceo.html', lines=lines)

@app.route('/reseller/<int:reseller_id>')
def reseller(reseller_id):
    lines = get_db().get_ads_from(reseller_id)
    return render_template('reseller.html', reseller_id=reseller_id, lines=lines)

@app.route('/ad/<int:ad_id>')
def ad(ad_id):
    try:
        ad = get_db().get_ad(ad_id)
    except db.AdNotFound:
        return render_template('404.html'), 404

    return render_template('ad.html',
        ad_id = ad.id,
        image_url = url_for('static', filename=ad.afbeelding),
        link = ad.link)

@app.route('/adserv/<int:reseller_id>/<int:ad_id>')
def adserv(reseller_id, ad_id):
    try:
        ads = get_db().get_ad_from(reseller_id, ad_id)
    except:
        print(f'adserv: Ad {ad_id} not found for {reseller_id}.')
        ad = models.Ad(0, 'placeholder.png', '')
    
    #get_db().update_views(reseller_ad_id)
    return url_for('static', filename=ad.afbeelding, _external=True)
    #return send_file(url_for('static', filename=ad.afbeelding), mimetype='image/png')
    #return send_file('/static/placeholder.png', mimetype='image/png')
    #return send_static_file('placeholder.png')

@app.route('/adservtest/<int:reseller_ad_id>')
def adservtest(reseller_ad_id):
    return f"<img src='http://localhost:8080/adserv/{reseller_ad_id}'>"




app.run(host='127.0.0.1', port='8080', debug=True)