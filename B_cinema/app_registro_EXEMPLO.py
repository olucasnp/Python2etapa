# BLUEPRINT cinema — importar + registrar no app.py
from controllers.cinema_controller import cinema_bp
app.register_blueprint(cinema_bp)

# layout.html: url_for('cinema.index') → apelido "cinema" + função "index"
