from flask import render_template
from learn_italian_flask import app, db

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html', title="404"), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html', title="500"), 500 
