from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from forms.LoginForm import LoginForm
from forms.RegisterForm import RegisterForm
from forms.SearchForm import SearchForm
from forms.EditProfileForm import ProfileForm
from forms.OfferForm import OfferForm
from data.user import User
from data.offer import Offer
from api_module import StaticApi

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


# Все, что касается login
@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('LoginTemplate.html',
                               message="Wrong login or password",
                               form=form, title='Login')
    return render_template('LoginTemplate.html', form=form,
                           title='Login', message="")


# Регистрация
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('RegisterTemplate.html', title='Register',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.username == form.username.data).first():
            return render_template('RegisterTemplate.html', title='Register',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            username=form.username.data,
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()

        return redirect('/login')
    return render_template('RegisterTemplate.html', form=form,
                           title='Register')


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()

    if request.method == 'POST':
        lonlat = form.lonlat.data
        task = form.offer_name.data

        api = StaticApi([int(ll) for ll in lonlat.split(';')])

        url, tags = api.get_map(task)
        return render_template('Search.html', form=form,
                               map_url=url, tags=tags)

    return render_template('Search.html', form=form, map_url=None,
                           tags=None)


@app.route('/')
def main():
    return render_template('MainPage.html')


@app.route('/profile')
@login_required
def profile():
    session = db_session.create_session()
    user_tags = session.query(Offer).filter(Offer.user_id == current_user.id).all()
    return render_template('ProfilePage.html', user_tags=user_tags)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileForm()
    if request.method == 'POST':
        username = form.username.data
        email = form.email.data
        about = form.about.data

        session = db_session.create_session()
        if username != '' and session.query(User).filter(User.username == username, User.id != current_user.id).first():
            return render_template('EditProfilePage.html', form=form, message='This username is already registered')

        session = db_session.create_session()
        if email != '' and session.query(User).filter(User.email == email, User.id != current_user.id).first():
            return render_template('EditProfilePage.html', form=form, message='This email is already registered')

        user = session.query(User).filter(User.id == current_user.id).first()
        if username != '':
            user.username = username
        if email != '':
            user.email = email
        if about != '':
            user.about = about

        password = form.password.data
        repeat_password = form.repeat_password.data

        if len(password) >= 5 and password == repeat_password:
            user.set_password(password)

        session.commit()
        return redirect('/profile')

    return render_template('EditProfilePage.html', form=form, message='')


@app.route('/offer/<int:id>')
@login_required
def offer_page(id):
    session = db_session.create_session()
    offer = session.query(Offer).filter(Offer.id == id).first()
    if offer:
        return render_template('OfferTemplate.html', offer=offer)
    else:
        return redirect('/')


@app.route('/create_barter', methods=['GET', 'POST'])
@login_required
def create_barter():
    form = OfferForm()

    if request.method == 'POST':
        session = db_session.create_session()

        title = form.title.data
        lon, lat = form.lon.data, form.lat.data
        description = form.description.data

        new_offer = Offer(
            title=title,
            lon=lon,
            lat=lat,
            description=description,
            user_id=current_user.id
        )

        session.add(new_offer)
        session.commit()
        return redirect('/profile')

    return render_template('CreateOffer.html', form=form)


if __name__ == '__main__':
    db_session.global_init("db/data.sqlite")
    app.run(port=8080, host='127.0.0.1', debug=True)
