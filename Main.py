from flask import Flask, render_template, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'RRRV3'


@app.route('/')
def start():
    return redirect('/main_page')


@app.route('/main_page')
def load_main_page():
    return render_template('main_page.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)