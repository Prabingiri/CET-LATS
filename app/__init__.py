from flask import Flask

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# Tip - To install packages from a requirements.txt file, run pip install -r requirements.txt
if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")
print('ENV is set to: {0}'.format(app.config["ENV"]))

from app import views