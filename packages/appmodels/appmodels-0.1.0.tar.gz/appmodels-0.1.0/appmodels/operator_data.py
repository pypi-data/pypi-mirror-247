import datetime

from flask_mongoengine import MongoEngine

mongo_db = MongoEngine()
algo_list_ = ['3DES-CBC', '3DES-ECB', 'AES-CBC']


class TransportKeyLabels(mongo_db.DynamicDocument):
    meta = {'collection': 'transport_key_labels',
            'db_alias': 'default'
            }
    datetime = mongo_db.DateTimeField(default=datetime.datetime.utcnow)
    key_id = mongo_db.IntField(unique=True)
    algo = mongo_db.StringField(choices=algo_list_)
    key_label = mongo_db.StringField(unique=True)
    description = mongo_db.StringField(default="description")
    is_available = mongo_db.BooleanField(default=False)


class OPLabels(mongo_db.DynamicDocument):
    meta = {'collection': 'op_labels',
            'db_alias': 'default'
            }
    datetime = mongo_db.DateTimeField(default=datetime.datetime.utcnow)
    op_id = mongo_db.IntField(unique=True)
    op_label = mongo_db.StringField(unique=True)
    description = mongo_db.StringField(default="description")
    is_available = mongo_db.BooleanField(default=False)
