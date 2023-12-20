from flask_mongoengine import MongoEngine
import datetime

from app_helpers.constants import AdditionalKeySets

mongo_db = MongoEngine()

profile_states_ = ['', 'Released', 'Downloaded', 'Installed', 'Error', 'Unavailable'
    , 'Available', 'Allocated', 'Linked', 'Confirmed', 'Unknown', 'Churn']
notif_profile_states_ = ['', 'Error', 'Installed', 'Enabled', 'Disabled', 'Deleted', 'Unknown']

profile_class_ = ['operational', 'provisional', 'test']
_status = ["WIP", "Lock", 'BAP_Approved', 'Obsolete']
_additional_key_sets = {AdditionalKeySets.KEY_SET_03: {'kic03', 'kid03', 'kik03'}, AdditionalKeySets.KEY_SET_04: {'kic04',
                                                                                                               'kid04',
                                                                                                               'kik04'},
                        AdditionalKeySets.KEY_SET_05: {'kic05', 'kid05', 'kik05'}, AdditionalKeySets.KEY_SET_06: {'kic06',
                                                                                                               'kid06',
                                                                                                               'kik06'},
                        AdditionalKeySets.KEY_SET_07: {'kic07', 'kid07', 'kik07'}, AdditionalKeySets.KEY_SET_08: {'kic08',
                                                                                                               'kid08',
                                                                                                               'kik08'},
                        AdditionalKeySets.KEY_SET_09: {'kic09', 'kid09', 'kik09'}, AdditionalKeySets.KEY_SET_0A: {'kic0a',
                                                                                                               'kid0a',
                                                                                                               'kik0a'},
                        AdditionalKeySets.KEY_SET_0B: {'kic0b', 'kid0b', 'kik0b'}, AdditionalKeySets.KEY_SET_0C: {'kic0c',
                                                                                                               'kid0c',
                                                                                                               'kik0c'},
                        AdditionalKeySets.KEY_SET_0D: {'kic0d', 'kid0d', 'kik0d'}, AdditionalKeySets.KEY_SET_0E: {'kic0e',
                                                                                                               'kid0e',
                                                                                                               'kik0e'},
                        AdditionalKeySets.KEY_SET_0F: {'kic0f', 'kid0f', 'kik0f'}}


class ProfilesTypes(mongo_db.DynamicDocument):
    # meta data that describe and provide information about data
    # to cahnge the name of the collection (to use mongengine with an existing data),create of class dictionary
    # called meta on the document and set collection to the name of the collection that you want your document calss to use
    meta = {'collection': 'profiles_types'
        , 'db_alias': 'default',
            'indexes': ['datetime', 'profile_type_id']
            # the element of index can be single field name ,tuple,dictionary
        , 'ordering': ['-datetime','profile_name']
            }
    datetime = mongo_db.DateTimeField(default=datetime.datetime.utcnow)
    profile_type_id = mongo_db.StringField(unique=True)
    profile_id = mongo_db.StringField()
    status = mongo_db.StringField(choices=_status)
    policy_id = mongo_db.StringField()
    carrier_id = mongo_db.StringField()
    profile_name = mongo_db.StringField(default="profilename")
    profile_class = mongo_db.StringField(choices=profile_class_)  # can choose(is limited) from the profile_class list
    spn = mongo_db.StringField()
    mcc_mnc = mongo_db.StringField(default="22201")
    gid_1 = mongo_db.StringField(default="FFFFFFFFFFFFFFFF")
    gid_2 = mongo_db.StringField(default="FFFFFFFFFFFFFFFF")
    description = mongo_db.StringField(default="Default meta with policy and owner and notification")
    tenant_name = mongo_db.StringField()
    profile_type_hash_value = mongo_db.StringField()
    created_user = mongo_db.StringField()
    meta_with_install_notif = mongo_db.BooleanField(default=True)
    carrier_app = mongo_db.BooleanField(default=False)
    meta_with_enable_notif = mongo_db.BooleanField(default=True)
    meta_with_delete_notif = mongo_db.BooleanField(default=True)
    meta_with_no_ppr = mongo_db.BooleanField(default=True)
    meta_with_disable_notif = mongo_db.BooleanField(default=True)
    meta_with_ppr_update_control_policy = mongo_db.BooleanField(default=False)
    meta_with_ppr1_no_disable_policy = mongo_db.BooleanField(default=False)
    meta_with_owner = mongo_db.BooleanField(default=True)
    meta_with_ppr2_no_delete_policy = mongo_db.BooleanField(default=False)
    with_confirm_code = mongo_db.BooleanField(default=False)
    meta_with_operator_id_gid2 = mongo_db.BooleanField(default=False)
    meta_with_operator_id_gid1 = mongo_db.BooleanField(default=False)
    
    

    def __unicode__(self):
        return self.profile_name


# define schema for a document that inherits from the class  Dynamic document
class InputBatches(
    mongo_db.DynamicDocument):  # using dynamicdocument no need to define the schema before insertion of data and we can change it
    meta = {'collection': 'input_batches'
        , 'db_alias': 'default',
            'indexes': ['datetime', 'batch_id', 'from_iccid', 'from_imsi']
            # to make querying fasters we use indexing(indexes)
        , 'ordering': ['-datetime']
            # ordering specified for queryset it will be applied when the queryset is created (+: for ascending; -:for descending)
            }
    # field are specified by adding field objects as class attributes
    batch_id = mongo_db.StringField(unique=True)  # to deffine the type of batch_id in mongoengine
    profile_type_id = mongo_db.StringField()
    total_sims = mongo_db.IntField(default=1)
    from_iccid = mongo_db.StringField(min_length=18, max_length=19)
    from_imsi = mongo_db.StringField()
    from_imsi2 = mongo_db.StringField()
    from_imsi3 = mongo_db.StringField()
    smsc = mongo_db.StringField()
    sume = mongo_db.StringField()
    op = mongo_db.StringField(min_length=32, max_length=32)
    input_file_name = mongo_db.StringField()
    total_expiry_days = mongo_db.IntField(default=365)
    is_op_encrypted = mongo_db.BooleanField(default=False)
    k4_label = mongo_db.StringField()
    input_header = mongo_db.StringField()
    additional_key_sets = mongo_db.ListField(mongo_db.StringField(choices=_additional_key_sets.keys()))
    constant_data = mongo_db.StringField(
        default='range_items:[(pin1,0000)],equal_items:[(pin2, second_pin_appl1, second_pin_appl2),(puk2,second_puk_appl1,second_puk_appl2),(kic1,kic2),(kid1,kid2),(kik1,kik2)]')
    impi_pattern = mongo_db.StringField(default='${IMSI}@ims.mnc${MNC}.mcc${MCC}.3gppnetwork.org')
    impu_pattern = mongo_db.StringField(default='sip:${IMSI}@ims.mnc${MNC}.mcc${MCC}.3gppnetwork.org')
    domain_pattern = mongo_db.StringField(
        default='ims.mnc${MNC}.mcc${MCC}.3gppnetwork.org')  # specified the text index for a field name by using $
    datetime = mongo_db.DateTimeField(default=datetime.datetime.utcnow)
    is_expired = mongo_db.BooleanField(default=False)
    list_msisdn = mongo_db.ListField(mongo_db.StringField())


class ImportFile(mongo_db.DynamicDocument):
    meta = {'collection': 'import_file'
        , 'db_alias': 'default',
            'indexes': ['var_to_encrypt', 'var_to_decrypt', 'path_of_import_file', 'var_k4label', 'var_batch_id',
                        'var_tenant']
        , 'ordering': ['-datetime']

            }
    var_to_encrypt = mongo_db.StringField()
    var_to_decrypt = mongo_db.StringField()
    path_of_import_file = mongo_db.StringField()
    var_k4label = mongo_db.StringField()
    var_batch_id = mongo_db.StringField()
    tenant_name = mongo_db.StringField()


def validate_string_length(min_length, max_length):
    def validator(value):
        if value and (len(value) < min_length or len(value) > max_length):
            from mongoengine import ValidationError
            raise ValidationError(f"String value must be between {min_length} and {max_length} characters.")
    return validator


class OutputFiles(mongo_db.DynamicDocument):
    meta = {'collection': 'output_files'
        , 'db_alias': 'default', 'indexes': ['datetime', 'batch_id', 'iccid', 'imsi']
        , 'ordering': ['-datetime']

            }
    batch_id = mongo_db.StringField(unique_with='iccid',
                                    default="batch01")  # iccid is unique and it releated to same specific batch id
    is_released = mongo_db.BooleanField(default=False)
    is_generated_data = mongo_db.StringField(default='yes')
    iccid = mongo_db.StringField(min_length=20, max_length=20, default="8929901012345678905F")
    imsi = mongo_db.StringField(default="299811123456789")
    imsi2 = mongo_db.StringField()
    imsi3 = mongo_db.StringField()
    opc = mongo_db.StringField(min_length=32, max_length=32, default="0102030405060708090A0B0C0D0E0F00")
    ki = mongo_db.StringField(min_length=32, max_length=32, default="000102030405060708090A0B0C0D0E0F")
    pin1 = mongo_db.StringField(min_length=4, max_length=16, default="0000")
    pin2 = mongo_db.StringField(min_length=4, max_length=16, default="1234")
    second_pin_appl1 = mongo_db.StringField(min_length=4, max_length=16, default="3456")
    second_pin_appl2 = mongo_db.StringField(min_length=4, max_length=16, default="5678")
    puk1 = mongo_db.StringField(min_length=4, max_length=16, default="00000000")
    puk2 = mongo_db.StringField(min_length=4, max_length=16, default="12345678")
    second_puk_appl1 = mongo_db.StringField(min_length=4, max_length=16, default="34567890")
    second_puk_appl2 = mongo_db.StringField(min_length=4, max_length=16, default="56789012")
    adm1 = mongo_db.StringField(min_length=4, max_length=16, default="12345678")
    adm2 = mongo_db.StringField(min_length=4, max_length=16, default="12345678")
    adm3 = mongo_db.StringField(min_length=4, max_length=16, default="12345678")
    adm4 = mongo_db.StringField(min_length=4, max_length=16, default="12345678")
    adm5 = mongo_db.StringField(min_length=4, max_length=16, default="12345678")
    acc = mongo_db.StringField(min_length=4, max_length=4, default="0001")
    msisdn = mongo_db.StringField()
    impi = mongo_db.StringField()
    impu = mongo_db.StringField()
    domain = mongo_db.StringField()
    kic1 = mongo_db.StringField(min_length=32, max_length=64, default="11223344556677881122334455667788")
    kid1 = mongo_db.StringField(min_length=32, max_length=64, default="11223344556677881122334455667788")
    kik1 = mongo_db.StringField(min_length=32, max_length=64, default="11223344556677881122334455667788")
    kic2 = mongo_db.StringField(min_length=32, max_length=64, default="11223344556677881122334455667788")
    kid2 = mongo_db.StringField(min_length=32, max_length=64, default="11223344556677881122334455667788")
    kik2 = mongo_db.StringField(min_length=32, max_length=64, default="11223344556677881122334455667788")
    kic03 = mongo_db.StringField(validation=validate_string_length(32, 64), required=False)
    kid03 = mongo_db.StringField(validation=validate_string_length(32, 64), required=False)
    kik03 = mongo_db.StringField(validation=validate_string_length(32, 64), required=False)
    kic04 = mongo_db.StringField(validation=validate_string_length(32, 64), required=False)
    kid04 = mongo_db.StringField(validation=validate_string_length(32, 64), required=False)
    kik04 = mongo_db.StringField(validation=validate_string_length(32, 64), required=False)
    kic05 = mongo_db.StringField(validation=validate_string_length(32, 64), required=False)
    kid05 = mongo_db.StringField(validation=validate_string_length(32, 64), required=False)
    kik05 = mongo_db.StringField(validation=validate_string_length(32, 64), required=False)
    kic06 = mongo_db.StringField(validation=validate_string_length(32, 64), required=False)
    kid06 = mongo_db.StringField(validation=validate_string_length(32, 64), required=False)
    kik06 = mongo_db.StringField(validation=validate_string_length(32, 64), required=False)
    kic07 = mongo_db.StringField(validation=validate_string_length(32, 64), required=False)
    kid07 = mongo_db.StringField(validation=validate_string_length(32, 64), required=False)
    kik07 = mongo_db.StringField(validation=validate_string_length(32, 64), required=False)
    kic08 = mongo_db.StringField(validation=validate_string_length(32, 64), required=False)
    kid08 = mongo_db.StringField(validation=validate_string_length(32, 64), required=False)
    kik08 = mongo_db.StringField(validation=validate_string_length(32, 64), required=False)
    kic09 = mongo_db.StringField(validation=validate_string_length(32, 64), required=False)
    kid09 = mongo_db.StringField(validation=validate_string_length(32, 64), required=False)
    kik09 = mongo_db.StringField(validation=validate_string_length(32, 64), required=False)
    kic0A = mongo_db.StringField(validation=validate_string_length(32, 64), required=False)
    kid0A = mongo_db.StringField(validation=validate_string_length(32, 64), required=False)
    kik0A = mongo_db.StringField(validation=validate_string_length(32, 64), required=False)
    kic0B = mongo_db.StringField(validation=validate_string_length(32, 64), required=False)
    kid0B = mongo_db.StringField(validation=validate_string_length(32, 64), required=False)
    kik0B = mongo_db.StringField(validation=validate_string_length(32, 64), required=False)
    kic0C = mongo_db.StringField(validation=validate_string_length(32, 64), required=False)
    kid0C = mongo_db.StringField(validation=validate_string_length(32, 64), required=False)
    kik0C = mongo_db.StringField(validation=validate_string_length(32, 64), required=False)
    kic0D = mongo_db.StringField(validation=validate_string_length(32, 64), required=False)
    kid0D = mongo_db.StringField(validation=validate_string_length(32, 64), required=False)
    kik0D = mongo_db.StringField(validation=validate_string_length(32, 64), required=False)
    kic0E = mongo_db.StringField(validation=validate_string_length(32, 64), required=False)
    kid0E = mongo_db.StringField(validation=validate_string_length(32, 64), required=False)
    kik0E = mongo_db.StringField(validation=validate_string_length(32, 64), required=False)
    kic0F = mongo_db.StringField(validation=validate_string_length(32, 64), required=False)
    kid0F = mongo_db.StringField(validation=validate_string_length(32, 64), required=False)
    kik0F = mongo_db.StringField(validation=validate_string_length(32, 64), required=False)
    datetime = mongo_db.DateTimeField(default=datetime.datetime.utcnow)


class Profiles(mongo_db.DynamicDocument):
    meta = {'collection': 'profiles'
        , 'indexes': ['iccid', 'datetime', 'to_datetime',
                      # Creating Issue; ESIMTT-237:
                      # 'from_datetime',
                      'batch_id',
                      'state',
                      # https://mongoengine.readthedocs.io/en/v0.9.0/guide/defining-documents.html#indexes
                      # https://www.mongodb.com/docs/manual/core/index-compound/
                      ("iccid", '-_id'),
                      ("state", '-_id'),
                      'matching_id', 'oid', 'matching_id_hashed'],
            # 'ordering': ['-datetime'],
            'db_alias': 'default'

            }
    datetime = mongo_db.DateTimeField()
    iccid = mongo_db.StringField(min_length=20, max_length=20)
    batch_id = mongo_db.StringField()
    state = mongo_db.StringField(choices=profile_states_)
    notif_state = mongo_db.StringField(choices=notif_profile_states_)
    notif_log = mongo_db.StringField(default="")
    matching_id = mongo_db.StringField(default="")
    matching_id_hashed = mongo_db.StringField(default="")
    linked_eid = mongo_db.StringField(default="")
    confirmation_code = mongo_db.StringField(default="")
    max_cc_retry = mongo_db.IntField(default=3)
    smds_address = mongo_db.StringField(default="")
    is_event_registered = mongo_db.BooleanField(default=False)
    last_eid = mongo_db.StringField(default="")
    last_trans_id = mongo_db.StringField(default="")
    last_device_brand = mongo_db.StringField()
    last_device_name = mongo_db.StringField()
    last_device_model = mongo_db.StringField()
    total_fetches = mongo_db.IntField(default=0)
    total_downloads = mongo_db.IntField(default=0)
    total_installs = mongo_db.IntField(default=0)
    total_errors = mongo_db.IntField(default=0)
    is_active = mongo_db.BooleanField(default=False)
    from_datetime = mongo_db.DateTimeField()
    to_datetime = mongo_db.DateTimeField()
    profile_meta = mongo_db.StringField(default="")
    profile_full = mongo_db.StringField(default="")
    rsp_version = mongo_db.StringField()

    @property
    def activation_code(self):
        return self.matching_id;


class ProfilesLogs(mongo_db.DynamicDocument):
    meta = {'collection': 'profiles_logs'
        , 'db_alias': 'default'
        , 'indexes': ['transaction_id', 'datetime', 'iccid'
                      ]
        , 'ordering': ['-datetime']
            }
    datetime = mongo_db.DateTimeField()
    rsp_version = mongo_db.StringField()
    duration = mongo_db.IntField()
    attempts = mongo_db.IntField(default=0)
    request_ip = mongo_db.StringField()
    transaction_id = mongo_db.StringField()
    method = mongo_db.StringField()
    curve_name = mongo_db.StringField()
    status = mongo_db.StringField()
    additional_info = mongo_db.StringField()
    error_message = mongo_db.StringField()
    iccid = mongo_db.StringField()
    imei = mongo_db.StringField()
    tac = mongo_db.StringField()
    device_brand = mongo_db.StringField()
    device_name = mongo_db.StringField()
    device_model = mongo_db.StringField()
    last_eid = mongo_db.StringField()
    batch_id = mongo_db.StringField()
    profile_type = mongo_db.StringField()
    selected_pki = mongo_db.StringField()
    auth_smdp_signature2 = mongo_db.StringField()
    euicc_cert = mongo_db.StringField()
    partial_log = mongo_db.StringField()
    last_datetime = mongo_db.DateTimeField()
    encoded_request = mongo_db.StringField()
    encoded_response = mongo_db.StringField()


class IccidByBatches(mongo_db.DynamicDocument):
    meta = {'collection': 'iccid_batches'
        , 'db_alias': 'default'
        , 'indexes': ['datetime', 'batch_id']
        , 'ordering': ['-datetime']
            }
    datetime = mongo_db.DateTimeField()
    batch_id = mongo_db.StringField()
    first_iccid = mongo_db.StringField()
    last_iccid = mongo_db.StringField()
    total_qty = mongo_db.IntField()
    profile_used = mongo_db.IntField()
    iccid_list = mongo_db.ListField(mongo_db.StringField())


class SummaryBatches(mongo_db.DynamicDocument):
    meta = {'collection': 'batches_summary'
        , 'db_alias': 'default'
        , 'indexes': ['batch_id']
        , 'ordering': ['-datetime']
            }
    batch_id = mongo_db.StringField(unique=True)
    total_sims = mongo_db.IntField(default=1)
    used_sims = mongo_db.IntField(default=0)
    released_sims = mongo_db.IntField(default=0)
    downloaded_sims = mongo_db.IntField(default=0)
    installed_sims = mongo_db.IntField(default=0)
    iccid_list = mongo_db.ListField(mongo_db.StringField())
    input_file_name = mongo_db.StringField()