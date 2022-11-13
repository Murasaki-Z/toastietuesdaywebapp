from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap

from flask_wtf import FlaskForm
from wtforms import widgets, RadioField, SelectMultipleField, SubmitField,SelectField
from notification import ConnectorCard
import time
SECRET_KEY = 'development'


DEVELOPMENT_ENV  = True

app = Flask(__name__
    , template_folder = '{}')




app_data = {
}

#global
filling_g = None
bread_g = None
cheese_g = None

bootstrap = Bootstrap()
app = Flask(__name__)
app.config.from_object(__name__)

bootstrap.init_app(app)

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()



class SimpleForm(FlaskForm):
    global filling_g
    global bread_g
    global cheese_g
    service = MultiCheckboxField('Label')
    fillings = RadioField('filling')
    breads   = RadioField('bread')

    # breads   = RadioField('bread', default = bread_g,
    #                    choices=[('White', 'White'), ('Brown', 'Brown'), ('Multigrain', 'Multigrain')])

@app.route('/')
def index():
    print('Index')
    return render_template('index.html', app_data=app_data)


@app.route('/about')
def about():
    return render_template('about.html', app_data=app_data)


@app.route('/service', methods = ['post', 'get'])
def service():

    global filling_g
    global bread_g
    global cheese_g

    print(1)
    cheese   = SimpleForm()
    bread    = SimpleForm()
    fillings = SimpleForm()
    cheese.service.choices   = [
    ('Cheese1', 'Cheese1'), ('Cheese2', 'Cheese2'), ('Cheese3', 'Cheese3')]

    fillings.fillings.choices=[
    ('Filling1', 'Filling1'), ('Filling2', 'Filling2'), ('Filling3', 'Filling3')]

    bread.breads.choices=[
    ('White', 'White'), ('Brown', 'Brown'), ('Multigrain', 'Multigrain')]
    print(2)

    # print(cheese.service.data)

    if request.method == 'POST':
        print(request.form)
        try:
            if request.form['order'] == 'Submit':
                print('POST')
                notify = ConnectorCard('{URL}')
                notify.text(bread=request.form['breads'], cheese = cheese.service.data
                    , fillings = request.form['fillings'])
                notify.title(request.form['name'] +' | '+ str(request.form['breads']) +' | '
                    + str(cheese.service.data) +' | '+ request.form['fillings'] )
                notify.send()
                # contact(name = request.form['name'])
                return redirect(url_for('contact', app_data=app_data, name = request.form['name']
                    , order = (str(request.form['breads']) +' | '
                    + str(cheese.service.data) +' | '+ request.form['fillings'])))
        except:
            pass

        #Handle Choices
        try:
            if request.form['choice']=='Chicken':
                print('Chicken')

                filling_g = 'Filling1'
                bread_g   = 'White'
                cheese_g  = 'Cheese1'
                cheese.service.data = ['Cheese1']
                fillings.fillings.data = 'Filling1'
                bread.breads.data = 'White'

                return render_template('service.html', app_data=app_data
                    , cheese = cheese.service.data, bread = bread
                    , fillings = fillings)

            if request.form['choice']=='Cheeze':
                filling_g = 'Filling2'
                bread_g   = 'White'
                return redirect(url_for('service'),app_data=app_data
                    , cheese = cheese, bread = bread
                    , fillings = fillings , choices = [filling_g, bread_g, cheese_g])

            if request.form['choice']=='Veggie':
                filling_g = 'Filling3'
                bread_g   = 'White'
                return redirect(url_for('service'),app_data=app_data
                    , cheese = cheese, bread = bread, fillings = fillings)
        except:
            pass


    print(10000)



    return render_template('service.html', app_data=app_data
        , cheese = cheese, bread = bread, fillings = fillings)


@app.route('/contact', methods = ['GET'])
def contact(name = ''):
    # print(request.args)
    name  = request.args['name']
    order = request.args['order']
    # print(url_for(service))
    return render_template('contact.html', app_data=app_data, name = name, order = order),{
    "Refresh": "5; url=http://127.0.0.1:5100/service"}
    # , {"Refresh": "1; service.html"}
        # return render_template('error.html'), {"Refresh": "1; url=https://google.com"}



if __name__ == '__main__':
    app.run(debug=DEVELOPMENT_ENV, port=5100)