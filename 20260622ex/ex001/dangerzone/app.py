from flask import Flask, render_template
from blueprints.member.routes import member_bp
from blueprints.dashboard.routes import dashboard_bp
from ai.camera_manager import init_camera

app = Flask(__name__)
app.secret_key = "dw-aiot5th-20260622"

app.register_blueprint(member_bp)
app.register_blueprint(dashboard_bp)

@app.route("/")
def home():
    return render_template('index.html')

if __name__ == '__main__':
    init_camera()
    app.run(
        host='0.0.0.0', 
        port=5000, 
        debug=False,
        threaded = True
    )