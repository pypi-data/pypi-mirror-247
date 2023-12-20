import os
import base64
from flask_login import UserMixin
from flask_mongoengine import MongoEngine
import datetime
import onetimepass
from mongoengine import ValidationError

from app_helpers.base_profiles import DEFAULT_PROFILE

email_cycle_ = ['Selected_days', 'Weekly', 'Two_weeks', 'Three_weeks', 'Monthly']
days_ = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
default_email_cycle_ = 'Weekly'
expend_expiry_date_category = ['Days','Month','Year']
access_ = {
    'user': 1,
    'admin': 2,
    'superadmin': 3
}

mongo_db = MongoEngine()
curve_names_ = ["brainpoolp256r1", "nistp256"]
key_purposes_ = ["DPtls", "DPauth", "DPpb"]
algo_list_ = ['3DES-CBC', '3DES-ECB', 'AES-CBC']
_runnable_states = ['Waiting', 'Accepted', 'Running', 'Error', 'Finished']
_runnable_scripts = ['GenerateFromImportFile', 'ExtendExpiryDaysBulk', 'GenerateOutputFiles', 'ExportOutputFiles',
                     'GenerateProfiles', 'GenerateAndReleaseProfiles', 'GenerateAndReleaseProfilesBasic', 'UpdateProfiles',
                     'ExportProfilesPdf', 'ExportProfilesCsv', 'DeleteOutputFiles', 'DeleteProfiles']
_runnable_old_scripts = ['OldSummaryByTenant', 'MissingummaryByTenant', 'IccidByBatches', 'InstalledBilling']
_automated_script = ['SummaryBatches', 'InstalledBilling']
_org_status = ['Activate', 'Inactive']
_ticket_type = ['eSIM Product Technical Issue', 'eSIM Customer Portal Issue']
_ticket_priority = ['Critical', 'High', 'Medium', 'Low']
_ticket_status = ['Received', 'Assigned', 'In Progress', 'Resolved', 'Closed', 'Reopened']
_ticket_default_status = 'Received'
_default_org_access = 'Inactive'
_org_activate = 'Activate'
_status = ["WIP", "Lock", 'BAP_Approved', 'Obsolete']
variables_choices = ["iccid","imsi","imsi2","imsi3","opc","ki","pin1","pin2","second_pin_appl1","second_pin_appl2",
                     "puk1","puk2","second_puk_appl1","second_puk_appl2","adm1","adm2","adm3","adm4","adm5","acc",
                     "msisdn","impi","impu","domain","kic1","kid1","kik1","kic2","kid2","kik2"]

_blacklist_status = ["Active", "Blacklisted"]
_blacklist_status_log = ["Active", "Blacklisted", "Not Found"]
_additional_notification_params = ["imei", "tac", "device_brand", "device_name", "device_model", "batch_id"]
_additional_notifications = ["handle_notif_enable", "handle_notif_disable", "handle_notif_delete", "handle_notif_install"]


class HsmKeyLabels(mongo_db.DynamicDocument):
    meta = {'collection': 'hsm_key_labels',
            'indexes': ['tenant_name',],
            'db_alias': 'default'  # to tell wich db
            }  # we use meta to tell wich db should the documents be attached in case we have diffrent DB
    datetime = mongo_db.DateTimeField(default=datetime.datetime.utcnow)
    key_label_hsm = mongo_db.StringField(unique=True)
    key_id = mongo_db.StringField(default="k4-keylabel", unique=True)
    tenant_name = mongo_db.StringField()
    key_length = mongo_db.StringField()
    username = mongo_db.StringField()
    country = mongo_db.StringField()
    key_status = mongo_db.StringField()
    network_key_type = mongo_db.StringField()
    key_location = mongo_db.StringField()
    key_algorithm = mongo_db.StringField()
    algorithm_mode = mongo_db.StringField()


class K4Label2(mongo_db.DynamicDocument):
    meta = {'collection': 'k4label'
        , 'db_alias': 'default'
            }
    label = mongo_db.StringField(choices=[])
    algo = mongo_db.StringField(choices=algo_list_)
    fields = mongo_db.StringField(default='ki,opc')

    def __unicode__(self):
        return self.label


class K4Label(mongo_db.EmbeddedDocument):
    label = mongo_db.StringField(choices=[])
    algo = mongo_db.StringField(choices=algo_list_)
    fields = mongo_db.StringField(default='ki,opc')


class UserAbstract(UserMixin, mongo_db.DynamicDocument):
    meta = {'abstract': True}
    first_name = mongo_db.StringField()
    last_name = mongo_db.StringField()
    email = mongo_db.StringField(unique=True)
    password = mongo_db.StringField()
    expiration_date = mongo_db.DateTimeField(default=datetime.datetime.utcnow)
    can_create = mongo_db.BooleanField(default=False)
    can_edit = mongo_db.BooleanField(default=False)
    can_edit_keys = mongo_db.BooleanField(default=False)
    can_delete = mongo_db.BooleanField(default=False)
    can_export = mongo_db.BooleanField(default=False)
    can_view_details = mongo_db.BooleanField(default=False)
    can_import = mongo_db.BooleanField(default=False)
    can_duplicate = mongo_db.BooleanField(default=False)
    is_expired = mongo_db.BooleanField(default=True)
    is_admin = mongo_db.BooleanField(default=False)
    is_view1 = mongo_db.BooleanField(default=False)
    is_view2 = mongo_db.BooleanField(default=False)
    is_view3 = mongo_db.BooleanField(default=False)
    is_view4 = mongo_db.BooleanField(default=False)
    insert_date = mongo_db.DateTimeField(default=datetime.datetime.utcnow)
    access = mongo_db.StringField(choices=access_)
    last_login = mongo_db.DateTimeField()
    support_team = mongo_db.BooleanField(default=False)
    role = mongo_db.ListField(mongo_db.StringField(choices=access_))

    def get_role(self, ):
        return self.role

    def __unicode__(self, ):
        return self.email

#for cutomer portal
class Roles(mongo_db.DynamicDocument):
    SUPER_ADMIN_ROLE_NAME = 'SuperAdmin'

    meta = {'collection': 'roles',
            }
    role = mongo_db.StringField()
    all_organization = mongo_db.BooleanField(default=False)
    full_access = mongo_db.BooleanField(default=False)
    related_organizations = mongo_db.ListField(mongo_db.StringField())
    audience = mongo_db.StringField()


class Role(mongo_db.DynamicDocument):
    name = mongo_db.StringField(unique=True)
    page_permissions = mongo_db.DictField()
    view_app1 = mongo_db.BooleanField(default=False)
    view_app2 = mongo_db.BooleanField(default=False)
    view_app3 = mongo_db.BooleanField(default=False)
    
    def get_permissions(self, key, subkey):
        try:
            return self.page_permissions.get(key, {}).get(subkey, [])
        except AttributeError:
            return []
    
    @classmethod
    def get_superadmin_role(cls):
        # Check if the "superadmin" role exists
        superadmin_role = cls.objects(name="superadmin").first()
        if not superadmin_role:
            # If it doesn't exist, create it with default permissions
            superadmin_role = cls(name="superadmin", page_permissions={})
            superadmin_role.save()
        return superadmin_role
    
class UserAbstractModified(UserMixin, mongo_db.DynamicDocument):
    meta = {'abstract': True}
    first_name = mongo_db.StringField()
    last_name = mongo_db.StringField()
    email = mongo_db.StringField(unique=True)
    password = mongo_db.StringField()
    expiration_date = mongo_db.DateTimeField(default=datetime.datetime.utcnow)
    insert_date = mongo_db.DateTimeField(default=datetime.datetime.utcnow)
    last_login = mongo_db.DateTimeField()
    support_team = mongo_db.BooleanField(default=False)
    is_expired = mongo_db.BooleanField(default=True)

    def __unicode__(self, ):
        return self.email

class User(UserAbstractModified):
    meta = {'collection': 'admin_user',
            }
    automated_email = mongo_db.BooleanField(default=False)
    role_object = mongo_db.ReferenceField(Role)

    def get_role(self):
        return self.role_object.name if self.role_object else "guest"

    def save(self, *args, **kwargs):
        # Check if the user has a role assigned, if not, assign the "guest" role.
        if not self.role_object and self.email != "admin@montyholding.com":
            try:
                guest_role = Role.objects.get(name="guest")
                guest_role.view_app3=True    
            except Role.DoesNotExist:
                guest_role = Role(name="guest", view_app3=True)
                
            guest_role.save()
            self.role_object = guest_role                
        super(User, self).save(*args, **kwargs)


class UsersPortal(UserAbstractModified):
    meta = {'collection': 'portal_user',
            }
    user_name = mongo_db.StringField()
    user_role = mongo_db.StringField()
    org_code = mongo_db.StringField()
    organization_name = mongo_db.StringField()
    is_active = mongo_db.BooleanField(default=True)
    automated_email = mongo_db.BooleanField(default=True)
    datetime = mongo_db.DateTimeField(default=datetime.datetime.utcnow)
    audience = mongo_db.StringField()
    user_created_by = mongo_db.StringField()
    user_updated_by = mongo_db.StringField()
    token_identifier = mongo_db.StringField(default=None)
    has_salt =  mongo_db.BooleanField(default=False)
    otp_secret= mongo_db.StringField(default=None)
    display_activation_code =  mongo_db.BooleanField(default=True)


class UserPortal(UserAbstractModified):
    meta = {'collection': 'admin_user',
            }
    password_history = mongo_db.ListField(mongo_db.StringField())
    automated_email = mongo_db.BooleanField(default=False)
    email_cycle = mongo_db.StringField(choices=email_cycle_, default=default_email_cycle_)
    days_to_send = mongo_db.ListField(mongo_db.StringField(choices=days_))
    start_sending_email = mongo_db.DateTimeField()
    email_to_send = mongo_db.DateTimeField()
    last_email_sent = mongo_db.DateTimeField()


class PrivilegesRoles(mongo_db.DynamicDocument):
    meta = {'collection': 'privilegesroles',
            }
    actions = mongo_db.StringField()
    url = mongo_db.StringField()
    access = mongo_db.ListField(mongo_db.StringField(choices=access_))


class Actions(mongo_db.DynamicDocument):
    meta = {'collection': 'actions',
            }
    actions = mongo_db.StringField()
    collection = mongo_db.StringField()
    access = mongo_db.ListField(mongo_db.StringField(choices=access_))
    depend_on_tenant = mongo_db.BooleanField(default=False)
    show_count = mongo_db.BooleanField(default=True)


class OperatorInfoState(mongo_db.DynamicDocument):
    meta = {'collection': 'operator_info_state'
        , 'indexes': [{'fields': ('datetime', 'tenant_name'), 'unique': True}]
        , 'ordering': ['-datetime', 'tenant_name']
            }
    datetime = mongo_db.DateTimeField(default=datetime.datetime.utcnow)
    tenant_name = mongo_db.StringField()
    total_first_installed = mongo_db.IntField(default=0)
    total_final_downloaded = mongo_db.IntField(default=0)
    total_final_installed = mongo_db.IntField(default=0)
    total_final_errors = mongo_db.IntField(default=0)
    total_final_released = mongo_db.IntField(default=0)
    total_final_unavailable = mongo_db.IntField(default=0)
    total_final_available = mongo_db.IntField(default=0)
    total_final_allocated = mongo_db.IntField(default=0)
    total_final_linked = mongo_db.IntField(default=0)
    total_final_confirmed = mongo_db.IntField(default=0)
    total_final_unknown = mongo_db.IntField(default=0)
    total_final_profiles = mongo_db.IntField(default=0)


class AdditionalNotification(mongo_db.EmbeddedDocument):
    notification_point = mongo_db.StringField(choices=_additional_notifications)
    notification_point_id = mongo_db.IntField()


class OperatorInfo(mongo_db.DynamicDocument):
    meta = {'collection': 'operator_info'
            }
    op_name = mongo_db.StringField(unique=True)
    tenant_name = mongo_db.StringField(unique=True)
    op_country = mongo_db.StringField()
    smdp_addr = mongo_db.StringField(unique=True, default="*.rsp.instant-connectivity.com")
    portal_addr = mongo_db.StringField(unique=True, default="*.instant-connectivity.net")
    var_out = mongo_db.StringField(
        default='iccid,imsi,opc,ki,pin1,pin2,second_pin_appl1,puk1,puk2,second_puk_appl1,adm1,kic1,kid1,kik1,kic2,kid2,kik2')
    decrypt_before_export = mongo_db.StringField(default='imsi')
    allow_es2plus = mongo_db.BooleanField(default=False)
    es2plus_allowed_variables = mongo_db.ListField(mongo_db.StringField(choices=variables_choices))
    send_download_progress_info = mongo_db.BooleanField(default=False)
    use_vpn = mongo_db.BooleanField(default=False)
    op_domain = mongo_db.StringField()
    notification_fri = mongo_db.StringField()
    notification_fci = mongo_db.StringField()
    additional_notification_params = mongo_db.ListField(mongo_db.StringField(choices=_additional_notification_params))
    additional_notifications = mongo_db.ListField(mongo_db.EmbeddedDocumentField(AdditionalNotification))
    allow_iccid_churn = mongo_db.BooleanField(default=False)
    allow_blacklist = mongo_db.BooleanField(default=False)

    op_oid = mongo_db.StringField(unique_with='tenant_name')
    op_fri = mongo_db.StringField(unique_with='tenant_name')
    op_fci = mongo_db.StringField(unique_with='tenant_name')
    op_auth_ci = mongo_db.StringField(unique_with='tenant_name')
    output_file_export = mongo_db.ListField(mongo_db.EmbeddedDocumentField(K4Label))
    pdf_split_volume = mongo_db.IntField(min_value=1, default=1000)
    one_qr_per_page = mongo_db.BooleanField(default=False)
    pdf_var_out = mongo_db.StringField(default='iccid')
    public_key = mongo_db.StringField(default="""-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: BCPG v1.63

mQSuBF6hl4YRDAD2pcq20p79nIfBk1Wr8QV2jGdPNhmSzJwscRKfT4/hG/QKx6DB
lvcxFON48B8N3Q5XUvhzX7lzKG7haY6alyT7ldRaUomtJ2pRu4L4DrRBtFaw1f8p
sbtQfaUlNbhI2SqedGfIjB46LLm1doDSVcWqgbdRE8qV+lsYcTZIbi6pwtTjlTfC
hQNSo5xOYOlFyWbSqm37SbQl9ByJ4+a8x3M2Nfj0+kT4EZc7WG5S8hDmFVfu1iD1
Y9NmP6xeyl3i3bTCTD7bOcDsIK6J3wauNxR41sRpAKwyhiEcvqaUB4DXAok4hI5p
Je1vrJPF2FqZFHV9lEtOlHBgKhl1cqODz3tNUPuUql1j7CqaquS9roUFYFHTQ2zN
AllBr1w2Ju2T2oTWz4LthgYRnzsiZnhpRtDltGQPTxxUPhMfJJJaXKUKcKXlLydP
M5hy53nHCf8gdwhvUI9UBy7YGpXd2c1jffytuPCwjEwzOVjwklaDefk4AV6eB9NX
p+v/mXkNTc9hnbkBAOd5+f0gqj2r9h748BGt6UK2BgRWajwOwX0HRizZfnezC/9J
HqpaoYbTAVnOrTNb8VAZhcbFl6B/3G5px7CSZ5tN18ONimyFo6p7KmZHUYLsOj3/
pNs2DUQGmKzo2B5qlGkP8qVEEgABEXa6uT+I9UD2exmvERHSY2t4gyorn1+MzniF
jsISQxLDZWa528Z+SgJ8/pR7yQWK9HtRIBjsna73lgexCeUsGjoklnfdWkGjrc15
438ZwSI1EasHF+UVr1BFJjTJ4GPdcUR+u5vLIzBVPtgk7z1YsGEWUr+Wnq2JpNIM
Py/lybog1leuL8VXYBXn3k9CV4/ANRHX5PCOVjQzDTDAbHCoyw8eiXYSrUq7Mjsb
/s3THog/5DabKYDvihb5R7NVtI4geBwuKu4DJ4+91nVoPzp5hren+mzxJBY88gRt
GD4A5cqKhbO7MUnnMFUt4lGJGb6YHtEo7vnuP0le24nlfg5Z3cXXQzNkxX1Bpopm
iGWtIXuRTf/BFKafAgjdhUDXbvHwgv7IdGJDaRfL3VTxph472gTd7UZgFvw8plkL
/2KdmLgS5jiyDLRKnXnUKTn2AYfN563I0Zo+8iFf7zxi/ZzYxT2+mcLMwmQRiAZb
dDvTmUWISNnTZtQu8tDAwOef5kzdJXUH89rVZzjW+URejHjBb1AmY9Suug+Uhc0O
y8OKdl9xyJzqcohLtINsCN3/gQHbyyfaHSGH9vWzixKrCBo4/1i4pl7zaAuMYwZW
I+X/MH73wfoYYFeOL7p6JC8YIudLpW5rzYZiA+rk+CHM64zHmY/vlaxmj3Hj0Mqy
IHFbWviSPop1vfxHza5Vf3/fQqEyraxnghQ0M+B9nlc9W493HVY/FzTP/898FIY+
lGIkYbbFRC8E2724UIAoqfP5AvloHoyb+vkMdxBPSZZga33+L/8bZkaepGGz6g5r
eWx9/hdhVnGkuGWaXaBJh6E//1fVWJNnBiUHhCHuEpq06xpItpXFWWD4qoUisFTf
a5ea9tvhnpENCKtT9j0bXKAtt9tczImQyXTqp/O87j4xak9v1kWShAwYAzR1G3Db
m7QgZmFyb3VrIDxmYXJvdWsudGFiYmFsQGdtYWlsLmNvbT6IXgQTEQoABgUCXqGX
hgAKCRAzpTNEMJp6Ji3GAQCxvgpIB+CzyhqPaGU9i2gIynVxy7L5IR6gzPVdLBa9
tQD/YT/QVqoebIbhOShy0C/U6dMIzQG3z5q6E9nZoT0MIl+5AQ0EXqGXhhAEAP//
////////yQ/aoiFowjTExmKLgNwc0SkCTgiKZ8x0Agu+pjsTmyJRSgh5jjQE3e+V
GbPNOkMbMCsKbfJfFDdP4TVtbVHCReSFtXZiXn7G9ExC6aY37WsL/1y29Aa37e44
a/taiZ+lrp8kEXxLH+ZJKGZR7OZTgf//////////AAICBADzvuHfjtbb81BnAplG
OokQP+wzHeHvPYKRHFkO35++G6mrRBgqQlhR+mvbWZlebfXTKU+aNV8tPD93KBuZ
mdQAU+BxUN4CG9h/sNZxrKqPi5A580TppGGuRNUMmP7Kr1hpapBpecjMvhaDK3Nb
qlXtxW6MyOTaECBBgeay3Rr8FYheBBgRCgAGBQJeoZeGAAoJEDOlM0QwmnomcBwB
AMQj1Sx5tLwaZRQQcAVczRZqy7Z3NpVl9WRYBnaK3BuCAQCZbxygvOfvyZMc9z0E
T5248sGn2XDFeBZ4XNO2MAEFtA==
=picO
-----END PGP PUBLIC KEY BLOCK-----""")
    datetime = mongo_db.DateTimeField(default=datetime.datetime.utcnow)
    total_init = mongo_db.IntField(default=0)
    total_fetches = mongo_db.IntField(default=0)
    total_downloads = mongo_db.IntField(default=0)
    total_installs = mongo_db.IntField(default=0)
    total_errors = mongo_db.IntField(default=0)
    total_first_installed = mongo_db.IntField(default=0)
    total_final_downloaded = mongo_db.IntField(default=0)
    total_final_installed = mongo_db.IntField(default=0)
    total_final_errors = mongo_db.IntField(default=0)
    total_final_released = mongo_db.IntField(default=0)
    total_final_unavailable = mongo_db.IntField(default=0)
    total_final_available = mongo_db.IntField(default=0)
    total_final_allocated = mongo_db.IntField(default=0)
    total_final_linked = mongo_db.IntField(default=0)
    total_final_confirmed = mongo_db.IntField(default=0)
    total_final_unknown = mongo_db.IntField(default=0)
    total_final_profiles = mongo_db.IntField(default=0)

    def clean(self):
        names = [notification.notification_point for notification in self.additional_notifications]
        if len(names) != len(set(names)):
            raise ValidationError("Duplicate custom notification names are not allowed.")


class HsmEcKeyPairs(mongo_db.DynamicDocument):
    meta = {'collection': 'hsm_ec_key_pairs'
        , 'db_alias': 'default'
            }
    datetime = mongo_db.DateTimeField(default=datetime.datetime.utcnow)
    key_purpose = mongo_db.StringField(choices=key_purposes_)
    is_test = mongo_db.BooleanField(default=True)
    curve_name = mongo_db.StringField(choices=curve_names_)
    pk_key_label_hsm = mongo_db.StringField()
    sk_key_label_hsm = mongo_db.StringField()
    total_usage = mongo_db.IntField(default=0)
    description = mongo_db.StringField(default="description")
    is_available = mongo_db.BooleanField(default=False)
    cert = mongo_db.StringField()


class RspVersions(mongo_db.DynamicDocument):
    meta = {'collection': 'rsp_versions'
        , 'indexes': ['datetime']
        , 'ordering': ['-datetime']
            }
    datetime = mongo_db.DateTimeField(default=datetime.datetime.utcnow)
    host_name = mongo_db.StringField()
    build_number = mongo_db.IntField()
    commit_hash = mongo_db.StringField()
    commit_msg = mongo_db.StringField()
    author_name = mongo_db.StringField()
    relative_date = mongo_db.StringField()
    affected_files = mongo_db.StringField()


class UnpersonalizedProfiles(mongo_db.DynamicDocument):
    meta = {'collection': 'unpreson_profiles'
        , 'indexes': ['datetime', 'profile_id']
        , 'ordering': ['-datetime', 'profile_id']
            }
    datetime = mongo_db.DateTimeField(default=datetime.datetime.utcnow)
    profile_id = mongo_db.StringField(unique=True)
    description = mongo_db.StringField()
    profile_hex = mongo_db.StringField()
    tenant_name = mongo_db.StringField()
    status = mongo_db.StringField(choices=_status)
    unpersonalized_profiles_hash = mongo_db.StringField()
    created_user = mongo_db.StringField()


class CarrierMetadata(mongo_db.DynamicDocument):
    meta = {'collection': 'carrier_metadata'
        , 'indexes': ['datetime', 'carrier_id']
        , 'ordering': ['-datetime', 'carrier_id']
            }
    datetime = mongo_db.DateTimeField(default=datetime.datetime.utcnow)
    carrier_id = mongo_db.StringField(unique=True)
    description = mongo_db.StringField()
    hash = mongo_db.StringField()

    package_name = mongo_db.StringField()
    permission_mask = mongo_db.StringField(default="0000000000000001")


class ProfileDownloadPolicies(mongo_db.DynamicDocument):
    meta = {'collection': 'profile_download_policies'
        , 'indexes': ['datetime', 'profile_id']
        , 'ordering': ['-datetime', 'profile_id']
            }
    datetime = mongo_db.DateTimeField(default=datetime.datetime.utcnow)
    policy_id = mongo_db.StringField(unique=True)
    description = mongo_db.StringField()
    re_download = mongo_db.BooleanField(default=True)
    with_same_eid = mongo_db.BooleanField(default=True)
    was_deleted = mongo_db.BooleanField(default=True)
    max_installs = mongo_db.IntField(default=0)


class ErrorInfo(mongo_db.DynamicDocument):
    meta = {'collection': 'error_info'
        , 'indexes': ['error_message']
        , 'ordering': ['datetime']
            }

    error_message = mongo_db.StringField(unique=True)
    error_info = mongo_db.StringField()


class TacInfo(mongo_db.DynamicDocument):
    meta = {'collection': 'tac_info'
        , 'indexes': ['allocated_tac_number']
        , 'ordering': ['-allocation_date']
            }
    allocated_tac_number = mongo_db.StringField(unique=True)
    manufacturer = mongo_db.StringField()
    model_name = mongo_db.StringField()
    marketing_name = mongo_db.StringField()
    brand_name = mongo_db.StringField()
    allocation_date = mongo_db.DateTimeField()
    country_code = mongo_db.IntField(default=0)
    fixed_code = mongo_db.StringField()
    organization_id = mongo_db.IntField(default=0)
    device_type = mongo_db.StringField()
    bluetooth = mongo_db.StringField()
    nfc = mongo_db.StringField()
    wlan = mongo_db.StringField()
    removable_uicc = mongo_db.StringField()
    removable_euicc = mongo_db.StringField()
    non_removable_uicc = mongo_db.StringField()
    non_removable_euicc = mongo_db.StringField()
    sim_slot = mongo_db.StringField()
    imei_support = mongo_db.StringField()
    operating_system = mongo_db.StringField()
    oem = mongo_db.StringField()
    bands = mongo_db.StringField()
    five_g_bands = mongo_db.StringField()
    lpwan = mongo_db.StringField()
    radio_interface = mongo_db.StringField()
    datetime = mongo_db.DateTimeField(default=datetime.datetime.utcnow)


class RunnableBatches(mongo_db.DynamicDocument):
    meta = {'collection': 'runnable_batches'
        , 'indexes': ['datetime', {'fields': ('batch_id', 'script', 'tenant_name'), 'unique': True}]
        , 'ordering': ['-datetime']
            }
    datetime = mongo_db.DateTimeField(default=datetime.datetime.utcnow)
    batch_id = mongo_db.StringField()
    tenant_name = mongo_db.StringField()
    script = mongo_db.StringField(choices=_runnable_scripts)
    state = mongo_db.StringField(choices=_runnable_states)
    duration = mongo_db.FloatField()
    end_date = mongo_db.DateTimeField()
    affected_rows = mongo_db.IntField(default=0)
    success_rows = mongo_db.IntField(default=0)
    informer = mongo_db.StringField()
    acceptor = mongo_db.StringField()
    failure_reason = mongo_db.StringField()
    status = mongo_db.StringField()
    status_date = mongo_db.DateTimeField()
    from_iccid = mongo_db.StringField()
    to_iccid = mongo_db.StringField()


class RunnableScripts(mongo_db.DynamicDocument):
    meta = {'collection': 'runnable_scripts'
        , 'indexes': ['datetime']
        , 'ordering': ['-datetime']
            }
    datetime = mongo_db.DateTimeField(default=datetime.datetime.utcnow)
    script = mongo_db.StringField(choices=_runnable_old_scripts)
    state = mongo_db.StringField(choices=_runnable_states)
    tenant_name = mongo_db.StringField()
    from_date = mongo_db.DateTimeField()
    to_date = mongo_db.DateTimeField()
    duration = mongo_db.FloatField()
    end_date = mongo_db.DateTimeField()
    affected_rows = mongo_db.IntField(default=0)
    success_rows = mongo_db.IntField(default=0)
    informer = mongo_db.StringField()
    acceptor = mongo_db.StringField()
    failure_reason = mongo_db.StringField()
    status = mongo_db.StringField()
    status_date = mongo_db.DateTimeField()


class AppStatus(mongo_db.EmbeddedDocument):
    meta = {'abstract': True, 'collection': 'app_status'}
    app_name = mongo_db.StringField()
    status = mongo_db.StringField()
    status_code = mongo_db.StringField()
    info = mongo_db.StringField()
    datetime = mongo_db.DateTimeField(default=datetime.datetime.utcnow)

    def __unicode__(self):
        return self.app_name


class EmailSettings(mongo_db.DynamicDocument):
    meta = {'collection': 'email_settings',
            'indexes': ['email'],
            }
    email = mongo_db.StringField(unique=True)
    username = mongo_db.StringField()
    password = mongo_db.StringField()
    smtp_server = mongo_db.StringField()
    smtp_port = mongo_db.IntField()
    need_tls = mongo_db.BooleanField(default=False)


class Settings(mongo_db.DynamicDocument):
    meta = {'collection': 'settings',
            'indexes': ['identity_key'],
            }
    identity_key = mongo_db.StringField(unique=True)
    identity_key_new = mongo_db.StringField()
    identity_salt = mongo_db.StringField()
    identity_url = mongo_db.StringField()
    audience = mongo_db.StringField()
    portal_email = mongo_db.StringField()
    app = mongo_db.StringField()


class SummaryByTenant(mongo_db.DynamicDocument):
    meta = {'collection': 'tenant_summary'
        , 'indexes': [{'fields': ('datetime', 'tenant_name'), 'unique': True}]
        , 'ordering': ['-datetime']
            }
    script_datetime = mongo_db.DateTimeField(default=datetime.datetime.utcnow)
    datetime = mongo_db.DateTimeField()
    tenant_name = mongo_db.StringField()
    total_downloads = mongo_db.IntField(default=0)
    total_installs = mongo_db.IntField(default=0)
    total_errors = mongo_db.IntField(default=0)
    total_disable = mongo_db.IntField(default=0)
    total_enable = mongo_db.IntField(default=0)
    total_handle_notif = mongo_db.IntField(default=0)
    total_delete = mongo_db.IntField(default=0)
    total_cancel = mongo_db.IntField(default=0)
    total_init_auth = mongo_db.IntField(default=0)
    total_auth_client = mongo_db.IntField(default=0)
    total_error_matching_id=mongo_db.IntField(default=0)


class DownloadsForBillings(mongo_db.DynamicDocument):
    meta = {'collection': 'tenant_downloads'
        , 'indexes': [{'fields': ('datetime', 'iccid'), 'unique': True}]
        , 'ordering': ['-datetime']
            }
    datetime = mongo_db.DateTimeField(default=datetime.datetime.utcnow)
    tenant_name = mongo_db.StringField()
    total_downloads = mongo_db.IntField(default=0)
    iccid = mongo_db.StringField()
    first_download = mongo_db.DateTimeField()
    last_download = mongo_db.DateTimeField()


class InstalledForBillings(mongo_db.DynamicDocument):
    meta = {'collection': 'tenant_installed'
        , 'indexes': [{'fields': ('datetime', 'iccid'), 'unique': True}]
        , 'ordering': ['-datetime']
            }
    datetime = mongo_db.DateTimeField(default=datetime.datetime.utcnow)
    tenant_name = mongo_db.StringField()
    total_installed = mongo_db.IntField(default=0)
    iccid = mongo_db.StringField()
    first_installation = mongo_db.DateTimeField()
    last_installation = mongo_db.DateTimeField()
    max_installs = mongo_db.IntField(default=0)
    policy_id = mongo_db.StringField()
    policy_desc = mongo_db.StringField()
    remainder_installed = mongo_db.StringField()
    remainder_scan = mongo_db.IntField(default=0)


class NbofAttempts(mongo_db.DynamicDocument):
    meta = {'collection': 'tenant_installed'
        , 'indexes': [{'fields': ('datetime', 'iccid'), 'unique': True}]
        , 'ordering': ['-datetime']
            }
    datetime = mongo_db.DateTimeField(default=datetime.datetime.utcnow)
    tenant_name = mongo_db.StringField()
    total_installed = mongo_db.IntField(default=0)
    iccid = mongo_db.StringField()
    first_installation = mongo_db.DateTimeField()
    last_installation = mongo_db.DateTimeField()
    max_installs = mongo_db.IntField(default=0)
    policy_id = mongo_db.StringField()
    remainder_installed = mongo_db.IntField(default=0)


class OrganizationType(mongo_db.DynamicDocument):
    meta = {'collection': 'organization_type'
            }
    org_type = mongo_db.StringField()
    description = mongo_db.StringField()
    org_has_child = mongo_db.BooleanField(default=False)
    is_active = mongo_db.BooleanField(default=True)
    need_mnc = mongo_db.BooleanField(default=False)
    need_mcc = mongo_db.BooleanField(default=False)
    org_code_prefix = mongo_db.StringField()
    org_code_suffix = mongo_db.StringField()
    audience = mongo_db.StringField()

    def __unicode__(self):
        return self.org_type


class OrganizationInfo(mongo_db.DynamicDocument):
    meta = {'collection': 'organization_info'
            }
    create_date = mongo_db.DateTimeField(default=datetime.datetime.utcnow)
    org_name = mongo_db.StringField()
    org_email = mongo_db.StringField()
    org_code = mongo_db.StringField()
    org_type = mongo_db.StringField()
    status = mongo_db.StringField(choices=_org_status, default=_default_org_access)
    nb_child = mongo_db.IntField(default=0)
    organization_parent = mongo_db.StringField(default='')
    org_pname = mongo_db.StringField()
    org_url = mongo_db.StringField()
    bill_id = mongo_db.IntField(default=0)
    nb_invoice = mongo_db.IntField(default=0)
    org_address = mongo_db.StringField()
    org_country = mongo_db.StringField()
    nb_of_users = mongo_db.IntField(default=1)
    org_logo = mongo_db.BinaryField()
    org_logo_png = mongo_db.StringField()
    org_extension = mongo_db.StringField()
    mcc = mongo_db.StringField(default='')
    mnc = mongo_db.StringField(default='')
    org_language = mongo_db.StringField(default='en')
    has_access = mongo_db.StringField(choices=_org_status, default=_default_org_access)
    org_ticket_suffix = mongo_db.StringField(default='1')
    audience = mongo_db.StringField()
    qr_org_email = mongo_db.StringField()
    display_msisdn = mongo_db.BooleanField(default=False)
    msisdn_length = mongo_db.IntField(default=1)
    unavailable_email = mongo_db.BooleanField(default=False)
    unavailable_org_email = mongo_db.StringField()

    iccid_checked = mongo_db.BooleanField(default=False)
    activation_code_checked = mongo_db.BooleanField(default=False)
    pin1_checked = mongo_db.BooleanField(default=False)
    pin2_checked = mongo_db.BooleanField(default=False)
    puk1_checked = mongo_db.BooleanField(default=False)
    puk2_checked = mongo_db.BooleanField(default=False)
    support_mfa =  mongo_db.BooleanField(default=True)


class Tickets(mongo_db.DynamicDocument):
    meta = {'collection': 'tickets'
            }

    ticket_number = mongo_db.StringField(unique=True)
    org_code = mongo_db.StringField()
    ticke_type = mongo_db.StringField(choices=_ticket_type)
    priority = mongo_db.StringField(choices=_ticket_priority)
    status = mongo_db.StringField(choices=_ticket_status, default=_ticket_default_status)
    title = mongo_db.StringField()
    description = mongo_db.StringField()
    request_by = mongo_db.StringField()
    assigned_to = mongo_db.StringField()
    attachement = mongo_db.ListField(mongo_db.BinaryField())
    extension = mongo_db.ListField(mongo_db.StringField())
    create_date = mongo_db.DateTimeField(default=datetime.datetime.utcnow)
    responded_date = mongo_db.DateTimeField()
    resolved_date = mongo_db.DateTimeField()
    last_updated_time = mongo_db.DateTimeField()


class TicketLogs(mongo_db.DynamicDocument):
    meta = {'collection': 'ticket_logs'
        , 'ordering': ['-datetime']

            }
    ticket_log = mongo_db.StringField(unique=True)
    ticket_number = mongo_db.StringField()
    org_code = mongo_db.StringField()
    send_to = mongo_db.StringField()
    send_by = mongo_db.StringField()
    description = mongo_db.StringField()
    create_date = mongo_db.DateTimeField(default=datetime.datetime.utcnow)
    attachement = mongo_db.ListField(mongo_db.BinaryField())
    extension = mongo_db.ListField(mongo_db.StringField())


class AutomatedScripts(mongo_db.DynamicDocument):
    meta = {'collection': 'automated_scripts'
        , 'indexes': [{'fields': ('datetime', 'script'), 'unique': True}]
        , 'ordering': ['-datetime']
            }
    datetime = mongo_db.DateTimeField(default=datetime.datetime.utcnow)
    script = mongo_db.StringField(choices=_automated_script)
    state = mongo_db.StringField(choices=_runnable_states)
    duration = mongo_db.FloatField()
    end_date = mongo_db.DateTimeField()
    affected_rows = mongo_db.IntField(default=0)
    success_rows = mongo_db.IntField(default=0)
    failure_reason = mongo_db.StringField()
    status = mongo_db.StringField()

class IccidChurn(mongo_db.DynamicDocument):
    meta = {'collection': 'iccid_churn',
            'indexes': ['iccid', 'date', 'current_eid']
    }

    date = mongo_db.DateTimeField()
    username = mongo_db.StringField()
    iccid = mongo_db.StringField()
    current_status = mongo_db.StringField()
    current_eid = mongo_db.StringField()
    result = mongo_db.StringField()


class BatchIccidChurnLog(mongo_db.DynamicDocument):
    meta = {
        'collection':'batch_iccid_churn_log',
        'indexes':['username', 'date']
    }
    username = mongo_db.StringField()
    no_of_iccid = mongo_db.IntField(default=0)
    input_file_name = mongo_db.StringField(unique=True)
    date = mongo_db.DateTimeField()
    action = mongo_db.StringField()

class ExcelBatchIccidChurnLog(mongo_db.DynamicDocument):
    meta = {
        'collection':'excel_batch_iccid_churn_log'
        }

    iccid = mongo_db.StringField()
    previous_status = mongo_db.StringField()
    updated_to_status = mongo_db.StringField()
    date = mongo_db.StringField()
    username = mongo_db.StringField()
    batch_iccid_log_id = mongo_db.StringField()
    status = mongo_db.StringField()


class ExtendExpiryDateLog(mongo_db.DynamicDocument):
    meta = {
        'collection':'extend_expiry_date_log',
        'indexes':['username']
    }
    input_batch_name = mongo_db.StringField()
    category = mongo_db.StringField(choices=expend_expiry_date_category)
    extended_type = mongo_db.StringField()
    extended_timeline = mongo_db.IntField(default=0)
    total_expiry_days = mongo_db.IntField(default=0)
    request_creation_date = mongo_db.DateTimeField()
    username = mongo_db.StringField()
    approver_name = mongo_db.StringField()
    no_of_iccid = mongo_db.IntField(default=0)
    status = mongo_db.StringField()
    print_iccid = mongo_db.BooleanField(default=False)
    auto_extend = mongo_db.BooleanField(default=False)
    no_iccid_changed = mongo_db.IntField(default=0)

class ExtendExpiryDateIccidLog(mongo_db.DynamicDocument):
    meta = {
        'collection':'extend_expiry_date_iccid_log',
        'indexes':['input_batch_name']
    }
    input_batch_name = mongo_db.StringField()
    iccid = mongo_db.StringField()
    extend_expiry_date_log = mongo_db.StringField()

class ExtendExpiryDateIccidNotChangedLog(mongo_db.DynamicDocument):
    meta = {
        'collection':'extend_expiry_date_iccid_not_changed_log',
        'indexes':['input_batch_name']
    }
    input_batch_name = mongo_db.StringField()
    iccid = mongo_db.StringField()
    extend_expiry_date_log = mongo_db.StringField()


class EIDBlacklistingMain(mongo_db.DynamicDocument):
    meta = {
        'collection':'eid_blacklisting',
        'indexes':['eid']
    }

    eid = mongo_db.StringField()
    status = mongo_db.StringField(choices=_blacklist_status)
    device_type = mongo_db.StringField()
    brand_name = mongo_db.StringField()
    model_name = mongo_db.StringField()
    imei = mongo_db.StringField()
    tac = mongo_db.StringField()

class BatchEIDBlacklistingLog(mongo_db.DynamicDocument):
    meta = {
        'collection':'batch_eid_blacklisting_log',
        'indexes':['username', 'date']
    }
    username = mongo_db.StringField()
    no_of_eid = mongo_db.IntField(default=0)
    input_file_name = mongo_db.StringField(unique=True)
    date = mongo_db.DateTimeField()
    action = mongo_db.StringField()

class ExcelBatchEIDBlacklistingLog(mongo_db.DynamicDocument):
    meta = {
        'collection':'excel_batch_eid_blacklisting_log'
        }

    eid = mongo_db.StringField()
    previous_status = mongo_db.StringField(choices=_blacklist_status_log)
    updated_to_status = mongo_db.StringField(choices=_blacklist_status_log)
    date = mongo_db.StringField()
    username = mongo_db.StringField()
    batch_eid_log_id = mongo_db.StringField()
    status = mongo_db.StringField()


class ClientPortalLogs(mongo_db.DynamicDocument):
    meta = {
        'collection': 'client_portal_logs',
        'indexes': ['org_code', 'email']
    }
    datetime = mongo_db.DateTimeField(default=datetime.datetime.utcnow)
    email = mongo_db.StringField()
    model = mongo_db.StringField()
    api = mongo_db.StringField()
    api_method=mongo_db.StringField()
    description= mongo_db.StringField()
    error_message = mongo_db.StringField()
    org_code = mongo_db.StringField()
    org_name = mongo_db.StringField()
    page_name= mongo_db.StringField()


class Country(mongo_db.DynamicDocument):
    name = mongo_db.StringField(unique=True)

class MonthlyTransactionReport(mongo_db.DynamicDocument):
    meta = {
        'collection': 'monthly_transaction_report',
        'indexes': ['monthly_date',]
    }

    monthly_date = mongo_db.StringField()
    organization = mongo_db.StringField()
    unique_download = mongo_db.IntField(default=0)
    re_download = mongo_db.IntField(default=0)
    enable_count = mongo_db.IntField(default=0)
    disable_count = mongo_db.IntField(default=0)
    delete_count = mongo_db.IntField(default=0)
    stock_availability = mongo_db.IntField(default=0)

class UniqueDownloadPerMonth(mongo_db.DynamicDocument):
    meta = {
        'collection': 'unique_download_per_month',
        'indexes': ['monthly_date','organization']
    }

    monthly_date = mongo_db.StringField()
    iccid = mongo_db.StringField()
    organization = mongo_db.StringField()
