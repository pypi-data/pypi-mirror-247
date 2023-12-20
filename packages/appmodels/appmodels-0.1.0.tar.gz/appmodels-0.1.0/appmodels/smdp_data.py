import datetime

from flask_mongoengine import MongoEngine

mongo_db = MongoEngine()

profile_states_ = ['', 'Released', 'Downloaded', 'Installed', 'Error', 'Unavailable',
                   'Available', 'Allocated', 'Linked', 'Confirmed', 'Unknown']
notif_profile_states_ = ['', 'Error', 'Installed', 'Enabled', 'Disabled', 'Deleted', 'Unknown']

profile_class_ = ['operational', 'provisional', 'test']


class ProfileTypes(mongo_db.DynamicDocument):
    meta = {'collection': 'smdp_profile_types',
            'db_alias': 'default',
            'indexes': ['datetime', 'profile_type_id'],
            'ordering': ['profile_name']
            }
    profile_type_id = mongo_db.StringField(unique=True)
    datetime = mongo_db.DateTimeField(default=datetime.datetime.utcnow)
    description = mongo_db.StringField()
    re_down_allowed = mongo_db.BooleanField(default=True)
    re_down_with_same_eid = mongo_db.BooleanField(default=True)
    re_down_was_deleted = mongo_db.BooleanField(default=True)
    re_down_max_installs = mongo_db.IntField(default=0)
    carrier_id = mongo_db.StringField()
    profile_name = mongo_db.StringField(default="profile name")
    profile_class = mongo_db.StringField(choices=profile_class_)
    spn = mongo_db.StringField()
    mcc_mnc = mongo_db.StringField(default="22201")
    gid_1 = mongo_db.StringField(default="FFFFFFFFFFFFFFFF")
    gid_2 = mongo_db.StringField(default="FFFFFFFFFFFFFFFF")
    carrier_app = mongo_db.BooleanField(default=False)
    meta_with_install_notif = mongo_db.BooleanField(default=True)
    meta_with_enable_notif = mongo_db.BooleanField(default=True)
    meta_with_disable_notif = mongo_db.BooleanField(default=True)
    meta_with_delete_notif = mongo_db.BooleanField(default=True)
    meta_with_no_ppr = mongo_db.BooleanField(default=True)
    meta_with_ppr_update_control_policy = mongo_db.BooleanField(default=False)
    meta_with_ppr1_no_disable_policy = mongo_db.BooleanField(default=False)
    meta_with_ppr2_no_delete_policy = mongo_db.BooleanField(default=False)
    meta_with_owner = mongo_db.BooleanField(default=True)
    meta_with_operator_id_gid1 = mongo_db.BooleanField(default=False)
    meta_with_operator_id_gid2 = mongo_db.BooleanField(default=False)
    with_confirm_code = mongo_db.BooleanField(default=False)

    def __unicode__(self):
        return self.profile_name


class ProfileData(mongo_db.DynamicDocument):
    meta = {'collection': 'smdp_profile_data',
            'indexes': ['iccid', 'datetime', 'to_datetime', 'matching_id', 'oid'],
            'ordering': ['-datetime'],
            'db_alias': 'default'
            }
    datetime = mongo_db.DateTimeField()
    iccid = mongo_db.StringField(min_length=20, max_length=20)
    batch_id = mongo_db.StringField()
    state = mongo_db.StringField(choices=profile_states_)
    notif_state = mongo_db.StringField(choices=notif_profile_states_)
    notif_log = mongo_db.StringField(default="")
    matching_id = mongo_db.StringField(default="")
    linked_eid = mongo_db.StringField(default="")
    confirmation_code = mongo_db.StringField(default="")
    max_cc_retry = mongo_db.IntField(default=3)
    smds_address = mongo_db.StringField(default="")
    is_event_registered = mongo_db.BooleanField(default=False)
    last_eid = mongo_db.StringField(default="")
    last_trans_id = mongo_db.StringField(default="")
    total_fetches = mongo_db.IntField(default=0)
    total_downloads = mongo_db.IntField(default=0)
    total_installs = mongo_db.IntField(default=0)
    total_errors = mongo_db.IntField(default=0)
    is_active = mongo_db.BooleanField(default=False)
    to_datetime = mongo_db.DateTimeField()
    profile_meta = mongo_db.StringField(default="")
    profile_full = mongo_db.StringField(default="")

    @property
    def activation_code(self):
        return self.matching_id
