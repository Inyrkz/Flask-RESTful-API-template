'''used to store the setting of the app (database)'''
from flask import Flask

#creating an instance of the flask app
app = Flask(__name__)

#configuring the database
app.config['SQLALCHEMY_DATABASE_URL'] = 'postgres://urmvplnlinfrnw:f555a59e48eb360d84a441de9e21ed9714b48d8b68126369eaa660a802da7656@ec2-52-202-22-140.compute-1.amazonaws.com:5432/d9bke6t472udgq'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
