from flask import Flask, render_template, request
from blueprints.member.routes import member_bp
app = Flask(__name__)

app.secret_key = 'out#gtg@dgi876tehd'

app.register_blueprint(member_bp)

# http://127.0.0.1:5000
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')




