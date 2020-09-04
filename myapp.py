from flask import (Flask,
                   make_response,
                   redirect,
                   render_template,
                   abort, url_for, session)

from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand



from wtforms import (StringField,
					 IntegerField, 
					 SubmitField)
from wtforms.validators import DataRequired, Length

from flask_wtf import Form

from collections import OrderedDict


app = Flask(__name__, template_folder="templates")
manager = Manager(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app=app, db=db)
manager.add_command('db', MigrateCommand)




import os 
app.config["SECRET_KEY"] = "uezfhuizehfuhzefhzefzie347687U"
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'mesdonnees.sqlite')


class NouveauForm(Form):
	name = StringField("Ton nom !!!", validators=[DataRequired()])
	submit_button = SubmitField("Envoi")


# 1 user peut avoir plusieurs posts
# 1 post ne vient qu'un utilisateur



class Post(db.Model):
	__tablename__ = "posts"
	id_ = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey("users.id_"))
	
	def __repr__(self):
		return "Le Post num :  {} , nom : {}".format(self.id_, self.name)

class User(db.Model):
	__tablename__ = "users"
	id_ = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(30), unique=True, nullable=False)
	#email = db.Column(db.String(100), unique=True)
	#age = db.Column(db.String(100))
	posts = db.relationship("Post", backref="user")

	def __repr__(self):
		return "User n°{} name: {}".format(self.id_, self.username)



@app.route('/')
def bonjour():
    return render_template("home.html", 
		var1=session.get("name"))

@app.route('/login/', methods=['GET', 'POST'])
def myfonction():
	
	return render_template("autre_page.html", 
		var1=session.get("name"))



@app.route('/users/')
def all_users():
	return render_template('listing.html', liste=User.query.all())

@app.route('/posts/')
def all_posts():
	return render_template('listing.html', liste = Post.query.all())

@app.route('/test/<name>', methods=['GET', 'POST'])
def test(name):
	# if request.method == "GET":
	# 	pass
	# if request.method == "PUT":
	# 	pass
	# if request.method == "POST"
	# 	pass
	myform = NouveauForm()
	if myform.validate_on_submit():
		session['name'] = myform.name.data

		# je filtre dans ma db en recherche de user
		user_retrieved = User.query.filter_by(username=myform.name.data).first()
		print(user_retrieved)
		if user_retrieved is None:
			# if n'existe pas
			# je crée une nouvelle instance user
			user = User(username = myform.name.data)
			db.session.add(user)
			db.session.commit()
			# pour garder en mémoire
			session["connu"] = "Vous êtes inconnu, on vous ajoute !"
		else:
			session["connu"] = "Vous êtes connu de la bdd !"
		
		myform.name.data = ''

		return redirect(url_for('test', name=session.get('name')))



	contenu_html = "<h1> Salut toi ;) </h1>"
	
	dico = OrderedDict({
		"tâche1": "Faire la vaisselle",
		"tâche2": "Faire le ménage",
		"tâche3": "écouter Monsieur Bertin"
		})
	# presentation rendered 
	return render_template("index.html", var1=name, var2=contenu_html, dico=dico, form=myform, connu=session.get("connu"))


@app.route("/voiciunredirect/")
def unefonction():
    return redirect("myfonction")


@app.route('/user/<name>')
def trouve(name):
    # -----
    return "<h1>Hello <i>" + name + "</i></h1>"

#@app.route('/<path:nompath>')
# def test2(nompath):
#	return "<h1>Hello</h1>"


@app.route('/<path:nompath>')
def error_404(nompath):
	abort(404, "The page {} is not found".format(nompath))


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html', error_message=e), 404



if __name__ == "__main__":
    manager.run()
