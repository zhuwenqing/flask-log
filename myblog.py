from app import app
from flask_login import LoginManager
if __name__=='__main__':
    login_manager=LoginManager()
    login_manager.init_app(app)
    login_manager.login_view='login'
    app.run(host='0.0.0.0',debug='True')