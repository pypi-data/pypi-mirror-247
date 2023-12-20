import os
import base64
from flask_login import UserMixin
from flask_mongoengine import MongoEngine
import datetime
import onetimepass


mongo_db = MongoEngine()
_billing_cycle = ['weekly', 'monthly', 'quarterly']
_calcul_process = ['price_per_profile', 'price_bulk_profiles', 'reprice_per_profile', 'reprice_bulk_profiles']
_billing_status = ['Paid', 'Unpaid']

class Currency(mongo_db.DynamicDocument):
    meta = {'collection': 'currency'
        , 'db_alias': 'default'
    }
    currency_code = mongo_db.StringField(unique=True)
    currency_name = mongo_db.StringField()
    currency_number = mongo_db.IntField(default=0)

class CurrencyExchange(mongo_db.DynamicDocument):
    meta = {'collection': 'currency_exchange'
        , 'db_alias': 'default'
    , 'indexes': [{'fields': ('currency_name', 'currency_exchange_name', 'from_date', 'to_date'), 'unique': True}]
    , 'ordering': ['-to_date', 'currency_name']
    }
    currency_name = mongo_db.StringField()
    currency_rate = mongo_db.FloatField()
    currency_exchange_name = mongo_db.StringField()
    currency_exchange_rate = mongo_db.FloatField()
    from_date = mongo_db.DateTimeField(default=datetime.datetime.utcnow)
    to_date = mongo_db.DateTimeField(default=datetime.datetime.utcnow)

class OrganizationBill(mongo_db.DynamicDocument):
    meta = {'collection': 'organization_bill'
        , 'db_alias': 'default'
    , 'indexes': [{'fields': ('organization_name','destination_country', 'destination_operator', 'billing_cycle'), 'unique': True}]
    }
    bill_id = mongo_db.IntField(default=0)
    organization_name = mongo_db.StringField()
    destination_country = mongo_db.StringField()
    destination_operator = mongo_db.StringField()
    country_code = mongo_db.StringField()
    mcc = mongo_db.StringField()
    mnc = mongo_db.StringField()
    currency_name = mongo_db.StringField()
    currency_code = mongo_db.StringField()
    currency_rate = mongo_db.FloatField()
    currency_exchange_name = mongo_db.StringField()
    currency_exchange_rate = mongo_db.FloatField()
    from_date = mongo_db.DateTimeField(default=datetime.datetime.utcnow)
    to_date = mongo_db.DateTimeField(default=datetime.datetime.utcnow)
    profile_cost = mongo_db.FloatField()
    bulk_profile_cost = mongo_db.FloatField()
    new_profile_cost = mongo_db.FloatField()
    bulk_new_profile_cost = mongo_db.FloatField()
    effective_date = mongo_db.DateTimeField(default=datetime.datetime.utcnow)
    billing_cycle =  mongo_db.StringField(choices=_billing_cycle)
    invoice_state = mongo_db.StringField(choices=_billing_status)

class Invoices(mongo_db.DynamicDocument):
    meta = {'collection': 'invoices'
        , 'db_alias': 'default'
    , 'indexes': [{'fields': ('invoice_number', 'bill_number', 'billing_cycle'), 'unique': True}]
    }
    invoice_number = mongo_db.IntField()
    organization_name = mongo_db.StringField()
    billing_address = mongo_db.StringField()
    bank_account = mongo_db.StringField()
    mcc = mongo_db.StringField()
    mnc = mongo_db.StringField()
    invoice_created_date =  mongo_db.DateTimeField(default=datetime.datetime.utcnow)
    start_period = mongo_db.DateTimeField(default=datetime.datetime.utcnow)
    due_date = mongo_db.DateTimeField(default=datetime.datetime.utcnow)
    amount = mongo_db.FloatField()
    currency_code = mongo_db.StringField()
    invoice_state = mongo_db.StringField(choices=_billing_status)
    calcul_process = mongo_db.StringField(choices=_calcul_process)
    bill_number = mongo_db.IntField(default=0)
    billing_cycle = mongo_db.StringField(choices=_billing_cycle)
    profile_consumption_day = mongo_db.IntField(default=0)
    total_profile_consumption = mongo_db.IntField(default=0)



