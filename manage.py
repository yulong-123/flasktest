from flask import Flask

app = Flask(__name__)


@app.route('/index')
def index():
    return {
        "msg": "success",
        "data": "welcome to use flask"
    }


if __name__ == '__main__':
    app.run()
