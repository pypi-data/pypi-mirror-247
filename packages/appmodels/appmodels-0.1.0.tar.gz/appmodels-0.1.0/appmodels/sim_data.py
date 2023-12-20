from flask_mongoengine import MongoEngine
from app_helpers.base_profiles import DEFAULT_PROFILE
import datetime

mongo_db = MongoEngine()


class ProfileTemplates(mongo_db.DynamicDocument):
    meta = {'collection': 'sim_profile_templates',
            'indexes': ['datetime', 'profile_id'],
            'ordering': ['-datetime', 'profile_id']
            }
    datetime = mongo_db.DateTimeField(default=datetime.datetime.utcnow)
    profile_id = mongo_db.StringField(unique=True)
    description = mongo_db.StringField()
    profile_hex = mongo_db.StringField(default=DEFAULT_PROFILE)


class BatchOrders(mongo_db.DynamicDocument):
    meta = {'collection': 'sim_batch_orders',
            'db_alias': 'default',
            'indexes': ['datetime', 'batch_id', 'from_iccid', 'from_imsi'],
            'ordering': ['-datetime']
            }

    batch_id = mongo_db.StringField(unique=True)
    profile_template_id = mongo_db.StringField()
    total_sims = mongo_db.IntField(default=1)
    from_iccid = mongo_db.StringField(min_length=18, max_length=19)
    from_imsi = mongo_db.StringField()
    from_imsi2 = mongo_db.StringField()
    from_imsi3 = mongo_db.StringField()
    smsc = mongo_db.StringField()
    op = mongo_db.StringField(min_length=32, max_length=32)
    total_expiry_days = mongo_db.IntField(default=365)
    is_op_encrypted = mongo_db.BooleanField(default=False)
    k4_label = mongo_db.StringField()
    input_header = mongo_db.StringField()
    constant_data = mongo_db.StringField(default='range_items:[(pin1,0000)],equal_items:[(pin1, second_pin_appl1), '
                                                 '(pin2,second_pin_appl2),(puk1,second_puk_appl1),(puk2,'
                                                 'second_puk_appl2),(kic1,kic2),(kid1,kid2),(kik1,kik2)]')
    datetime = mongo_db.DateTimeField(default=datetime.datetime.utcnow)
    is_expired = mongo_db.BooleanField(default=False)
    list_msisdn = mongo_db.ListField(mongo_db.StringField())


common_string_field = {
    "min_length": 4,
    "max_length": 16
}

common_long_string_field = {
    "min_length": 32,
    "max_length": 64,
    "default": "11223344556677881122334455667788"
}

class SimData(mongo_db.DynamicDocument):
    meta = {'collection': 'sim_data',
            'db_alias': 'default',
            'indexes': ['datetime', 'batch_id', 'iccid', 'imsi'],
            'ordering': ['-datetime']
            }
    
    batch_id = mongo_db.StringField(unique_with='iccid', default="batch01")
    is_released = mongo_db.BooleanField(default="299811123456789")
    is_generated_data = mongo_db.StringField(default="299811123456789")
    iccid = mongo_db.StringField(min_length=20, max_length=20, default="8929901012345678905F")
    imsi = mongo_db.StringField(default="299811123456789")
    imsi2 = mongo_db.StringField()
    imsi3 = mongo_db.StringField()
    opc = mongo_db.StringField(min_length=32, max_length=32, default="0102030405060708090A0B0C0D0E0F00")
    ki = mongo_db.StringField(min_length=32, max_length=32, default="000102030405060708090A0B0C0D0E0F")
    pin1 = mongo_db.StringField(**common_string_field, default="0000")
    pin2 = mongo_db.StringField(**common_string_field, default="1234")
    second_pin_appl1 = mongo_db.StringField(**common_string_field, default="3456")
    second_pin_appl2 = mongo_db.StringField(**common_string_field, default="5678")
    puk1 = mongo_db.StringField(**common_string_field, default="00000000")
    puk2 = mongo_db.StringField(**common_string_field, default="12345678")
    second_puk_appl1 = mongo_db.StringField(**common_string_field, default="34567890")
    second_puk_appl2 = mongo_db.StringField(**common_string_field, default="56789012")
    adm1 = mongo_db.StringField(**common_string_field, default="12345678")
    adm3 = mongo_db.StringField(**common_string_field, default="12345678")
    acc = mongo_db.StringField(min_length=4, max_length=4, default="0001")
    msisdn = mongo_db.StringField()
    kic1 = mongo_db.StringField(**common_long_string_field)
    kid1 = mongo_db.StringField(**common_long_string_field)
    kik1 = mongo_db.StringField(**common_long_string_field)
    kic2 = mongo_db.StringField(**common_long_string_field)
    kid2 = mongo_db.StringField(**common_long_string_field)
    kik2 = mongo_db.StringField(**common_long_string_field)
    datetime = mongo_db.DateTimeField(default=datetime.datetime.utcnow)