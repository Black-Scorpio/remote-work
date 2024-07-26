from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random
from flask_bootstrap import Bootstrap5

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(model_class=Base)
db.init_app(app)
Bootstrap5(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    filter_location = request.args.get('filter')
    if filter_location:
        cafes = Cafe.query.filter(Cafe.location.ilike(f"%{filter_location}%")).order_by(Cafe.name).all()
    else:
        cafes = Cafe.query.order_by(Cafe.name).all()
    return render_template("index.html", cafes=cafes)



@app.route('/random', methods=['GET'])
def get_random_cafe():
    random_cafe = random.choice(Cafe.query.all())
    return jsonify(random_cafe.to_dict())


@app.route('/cafe', methods=['GET'])
def get_all_cafe():
    cafes = Cafe.query.order_by(Cafe.name).all()
    return jsonify([cafe.to_dict() for cafe in cafes])


@app.route('/search', methods=['GET'])
def find_cafe():
    location = request.args.get('loc').title()
    cafes = Cafe.query.filter_by(location=location).all()
    if not cafes:
        return jsonify({"error": "No Cafes found for the specified location"}), 404
    return jsonify([cafe.to_dict() for cafe in cafes])


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    if request.method == 'POST':
        new_cafe = Cafe(
            name=request.form.get("name"),
            map_url=request.form.get("map_url"),
            img_url=request.form.get("img_url"),
            location=request.form.get("location"),
            has_sockets=bool(request.form.get("sockets")),
            has_toilet=bool(request.form.get("toilet")),
            has_wifi=bool(request.form.get("wifi")),
            can_take_calls=bool(request.form.get("calls")),
            seats=request.form.get("seats"),
            coffee_price=request.form.get("coffee_price"),
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_cafe.html')


@app.route('/update-price/<int:cafe_id>', methods=['PATCH'])
def update_price(cafe_id):
    new_price = request.form.get('new_price')
    cafe = Cafe.query.get_or_404(cafe_id)
    cafe.coffee_price = new_price
    db.session.commit()
    return jsonify(response={"Success": f"{cafe.name} has a new coffee price of {new_price}"})


@app.route('/delete/<int:cafe_id>', methods=['POST'])
def delete_cafe(cafe_id):
    cafe = Cafe.query.get_or_404(cafe_id)
    db.session.delete(cafe)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
