"""
author : Ger-Rr
"""
import os
from dotenv import load_dotenv
from app import create_app
from app.extensions import db
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand

dotenv_path = os.path.join(os.path.dirname(__file__),'.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = create_app("development")
manager = Manager(app)
Migrate(app,db)
manager.add_command('db',MigrateCommand)




if __name__ == '__main__':
    manager.run()