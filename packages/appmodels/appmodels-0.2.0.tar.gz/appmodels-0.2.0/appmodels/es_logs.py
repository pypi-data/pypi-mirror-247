from flask_mongoengine import MongoEngine

from app_helpers.constants import NotificationStatus
from app_helpers.funcs import get_month_format

mongo_db = MongoEngine()
notification_statuses = [NotificationStatus.READY, NotificationStatus.PENDING, NotificationStatus.SENT]


class Es9plusLogsPerMethod(mongo_db.DynamicDocument):
    meta = {'collection': 'es9plus_logs_method',
            'db_alias': 'default',
            'indexes': ['begin_date', 'trans_id'],
            'ordering': ['-begin_date']
            }
    begin_date = mongo_db.DateTimeField()
    end_date = mongo_db.DateTimeField()
    duration = mongo_db.IntField()
    request_ip = mongo_db.StringField()
    trans_id = mongo_db.StringField()
    method = mongo_db.StringField()
    rsp_version = mongo_db.StringField()
    curve_name = mongo_db.StringField()
    status = mongo_db.StringField()
    additional_info = mongo_db.StringField()
    error_message = mongo_db.StringField()
    iccid = mongo_db.StringField()
    imei = mongo_db.StringField()
    tac = mongo_db.StringField()
    last_eid = mongo_db.StringField()
    batch_id = mongo_db.StringField()
    profile_type = mongo_db.StringField()
    selected_pki = mongo_db.StringField()
    auth_smdp_signature2 = mongo_db.StringField()
    euicc_cert = mongo_db.StringField()
    device_brand = mongo_db.StringField()
    device_name = mongo_db.StringField()
    device_model = mongo_db.StringField()
    server_challenge = mongo_db.StringField()
    partial_log = mongo_db.StringField()


class StatusCodeData(mongo_db.EmbeddedDocument):
    subjectCode = mongo_db.StringField()
    reasonCode = mongo_db.StringField()
    message = mongo_db.StringField()
    subjectIdentifier = mongo_db.StringField()


class FunctionExecutionStatus(mongo_db.EmbeddedDocument):
    status = mongo_db.StringField()
    statusCodeData = mongo_db.EmbeddedDocumentField(
        StatusCodeData)


class RspHeader(mongo_db.EmbeddedDocument):
    functionExecutionStatus = mongo_db.EmbeddedDocumentField(
        FunctionExecutionStatus)


class EuiccInfo1(mongo_db.EmbeddedDocument):
    svn = mongo_db.StringField()
    euiccCiPKIdListForVerification = mongo_db.ListField(mongo_db.StringField())
    euiccCiPKIdListForSigning = mongo_db.ListField(mongo_db.StringField())


class ServerSigned1(mongo_db.EmbeddedDocument):
    transactionId = mongo_db.StringField()
    euiccChallenge = mongo_db.StringField()
    serverAddress = mongo_db.StringField()
    serverChallenge = mongo_db.StringField()


class InitiateAuthenticationRequest(mongo_db.EmbeddedDocument):
    datetime = mongo_db.DateTimeField()
    request_ip = mongo_db.StringField()
    euiccInfo1 = mongo_db.StringField()
    smdpAddress = mongo_db.StringField()
    euiccChallenge = mongo_db.StringField()
    euicc_info1_details = mongo_db.EmbeddedDocumentField(EuiccInfo1)


class InitiateAuthenticationResponse(mongo_db.EmbeddedDocument):
    datetime = mongo_db.DateTimeField()
    header = mongo_db.EmbeddedDocumentField(RspHeader)
    transactionId = mongo_db.StringField()
    euiccCiPKIdToBeUsed = mongo_db.StringField()
    serverCertificate = mongo_db.StringField()
    serverSigned1 = mongo_db.StringField()
    serverSignature1 = mongo_db.StringField()
    server_signed1_details = mongo_db.EmbeddedDocumentField(ServerSigned1)


class AuthenticateResponseOk(mongo_db.EmbeddedDocument):
    transactionId = mongo_db.StringField()
    serverAddress = mongo_db.StringField()
    serverChallenge = mongo_db.StringField()
    profileVersion = mongo_db.StringField()
    svn = mongo_db.StringField()
    euiccCiPKIdListForVerification = mongo_db.ListField(mongo_db.StringField())
    euiccCiPKIdListForSigning = mongo_db.ListField(mongo_db.StringField())
    matchingId = mongo_db.StringField()
    imei = mongo_db.StringField()
    euiccSignature1 = mongo_db.StringField()
    eid = mongo_db.StringField()


class AuthenticateServerResponse(mongo_db.EmbeddedDocument):
    authenticateResponseOk = mongo_db.EmbeddedDocumentField(AuthenticateResponseOk)
    authenticateResponseError = mongo_db.StringField()


class AuthenticateClientRequest(mongo_db.EmbeddedDocument):
    datetime = mongo_db.DateTimeField()
    request_ip = mongo_db.StringField()
    transactionId = mongo_db.StringField()
    authenticateServerResponse = mongo_db.StringField()
    auth_server_resp_details = mongo_db.EmbeddedDocumentField(AuthenticateServerResponse)


class AuthenticateClientResponse(mongo_db.EmbeddedDocument):
    datetime = mongo_db.DateTimeField()
    header = mongo_db.EmbeddedDocumentField(RspHeader)
    transactionId = mongo_db.StringField()
    profileMetadata = mongo_db.StringField()
    smdpSigned2 = mongo_db.StringField()
    smdpSignature2 = mongo_db.StringField()
    smdpCertificate = mongo_db.StringField()


class GetBoundProfilePackageRequest(mongo_db.EmbeddedDocument):
    datetime = mongo_db.DateTimeField()
    request_ip = mongo_db.StringField()
    transactionId = mongo_db.StringField()
    prepareDownloadResponse = mongo_db.StringField()


class GetBoundProfilePackageResponse(mongo_db.EmbeddedDocument):
    datetime = mongo_db.DateTimeField()
    header = mongo_db.EmbeddedDocumentField(RspHeader)
    transactionId = mongo_db.StringField()
    boundProfilePackage = mongo_db.StringField()


class PendingNotification(mongo_db.EmbeddedDocument):
    transactionId = mongo_db.StringField()
    seqNumber = mongo_db.StringField()
    profileManagementOperation = mongo_db.StringField()
    notificationAddress = mongo_db.StringField()
    iccid = mongo_db.StringField()
    smdpOid = mongo_db.StringField()
    aid = mongo_db.StringField()
    simaResponse = mongo_db.StringField()
    bppCommandId = mongo_db.StringField()
    errorReason = mongo_db.StringField()
    euiccSignPIR = mongo_db.StringField()


class PendingOtherNotification(mongo_db.EmbeddedDocument):
    transactionId = mongo_db.StringField()
    pendingNotification = mongo_db.StringField()
    seqNumber = mongo_db.StringField()
    profileManagementOperation = mongo_db.StringField()
    notificationAddress = mongo_db.StringField()
    iccid = mongo_db.StringField()
    euiccNotificationSignature = mongo_db.StringField()
    euiccCertificate = mongo_db.StringField()
    eumCertificate = mongo_db.StringField()


class HandleNotificationRequest(mongo_db.EmbeddedDocument):
    datetime = mongo_db.DateTimeField()
    request_ip = mongo_db.StringField()
    transactionId = mongo_db.StringField()
    pendingNotification = mongo_db.StringField()
    pending_notification_details = mongo_db.EmbeddedDocumentField(PendingNotification)
    pending_notification_install = mongo_db.EmbeddedDocumentField(PendingOtherNotification)
    pending_notification_enable = mongo_db.EmbeddedDocumentField(PendingOtherNotification)
    pending_notification_disable = mongo_db.EmbeddedDocumentField(PendingOtherNotification)
    pending_notification_delete = mongo_db.EmbeddedDocumentField(PendingOtherNotification)


class CancelSessionRequest(mongo_db.EmbeddedDocument):
    datetime = mongo_db.DateTimeField()
    request_ip = mongo_db.StringField()
    transactionId = mongo_db.StringField()
    cancelSessionResponse = mongo_db.StringField()
    reason = mongo_db.StringField()


class CancelSessionResponse(mongo_db.EmbeddedDocument):
    datetime = mongo_db.DateTimeField()
    header = mongo_db.EmbeddedDocumentField(RspHeader)
    cancelSessionRequestEs9 = mongo_db.StringField()
    cancelSessionOk = mongo_db.StringField()


class Es9plusLogsPerTrans(mongo_db.DynamicDocument):
    meta = {'collection': 'es9plus_logs_trans',
            'db_alias': 'default',
            'indexes': ['begin_date', 'transaction_id'],
            'ordering': ['-begin_date']
            }
    begin_date = mongo_db.DateTimeField()
    end_date = mongo_db.DateTimeField()
    trans_id = mongo_db.StringField()
    request_ip = mongo_db.StringField()
    methods_list = mongo_db.ListField(mongo_db.StringField())
    init_auth_request = mongo_db.EmbeddedDocumentField(
        InitiateAuthenticationRequest)
    init_auth_response = mongo_db.EmbeddedDocumentField(
        InitiateAuthenticationResponse)
    auth_client_request = mongo_db.EmbeddedDocumentField(
        AuthenticateClientRequest)
    auth_client_response = mongo_db.EmbeddedDocumentField(
        AuthenticateClientResponse)
    get_b_profile_request = mongo_db.EmbeddedDocumentField(
        GetBoundProfilePackageRequest)
    get_b_profile_response = mongo_db.EmbeddedDocumentField(
        GetBoundProfilePackageResponse)
    handle_notif_request = mongo_db.EmbeddedDocumentField(
        HandleNotificationRequest)
    handle_notif_response = mongo_db.StringField()
    cancel_session_request = mongo_db.EmbeddedDocumentField(
        CancelSessionRequest)
    cancel_session_response = mongo_db.EmbeddedDocumentField(
        CancelSessionResponse)


class DownloadOrderRequest(mongo_db.EmbeddedDocument):
    datetime = mongo_db.DateTimeField()
    request_ip = mongo_db.StringField()
    eid = mongo_db.StringField()
    iccid = mongo_db.StringField()
    profileType = mongo_db.StringField()


class DownloadOrderResponse(mongo_db.EmbeddedDocument):
    datetime = mongo_db.DateTimeField()
    header = mongo_db.EmbeddedDocumentField(RspHeader)
    iccid = mongo_db.StringField()


class ConfirmOrderRequest(mongo_db.EmbeddedDocument):
    datetime = mongo_db.DateTimeField()
    request_ip = mongo_db.StringField()
    iccid = mongo_db.StringField()
    eid = mongo_db.StringField()
    matchingId = mongo_db.StringField()
    confirmationCode = mongo_db.StringField()
    smdsAddress = mongo_db.StringField()
    releaseFlag = mongo_db.StringField()


class ConfirmOrderResponse(mongo_db.EmbeddedDocument):
    datetime = mongo_db.DateTimeField()
    header = mongo_db.EmbeddedDocumentField(RspHeader)
    eid = mongo_db.StringField()
    matchingId = mongo_db.StringField()
    smdsAddress = mongo_db.StringField()


class CancelOrderRequest(mongo_db.EmbeddedDocument):
    datetime = mongo_db.DateTimeField()
    request_ip = mongo_db.StringField()
    iccid = mongo_db.StringField()
    eid = mongo_db.StringField()
    matchingId = mongo_db.StringField()
    finalProfileStatusIndicator = mongo_db.StringField()


class CancelOrderResponse(mongo_db.EmbeddedDocument):
    datetime = mongo_db.DateTimeField()
    header = mongo_db.EmbeddedDocumentField(RspHeader)


class ReleaseProfileRequest(mongo_db.EmbeddedDocument):
    datetime = mongo_db.DateTimeField()
    request_ip = mongo_db.StringField()
    iccid = mongo_db.StringField()


class ReleaseProfileResponse(mongo_db.EmbeddedDocument):
    datetime = mongo_db.DateTimeField()
    header = mongo_db.EmbeddedDocumentField(RspHeader)


class Es2plusLogs(mongo_db.DynamicDocument):
    meta = {'collection': 'es2plus_logs_' + get_month_format(),
            'db_alias': 'default',
            'indexes': ['datetime', 'iccid'],
            'ordering': ['-datetime']
            }
    datetime = mongo_db.DateTimeField()
    last_datetime = mongo_db.DateTimeField()
    iccid = mongo_db.StringField()
    request_ip = mongo_db.StringField()
    methods_list = mongo_db.ListField(mongo_db.StringField())
    download_order_request = mongo_db.EmbeddedDocumentField(
        DownloadOrderRequest)
    download_order_response = mongo_db.EmbeddedDocumentField(
        DownloadOrderResponse)
    confirm_order_request = mongo_db.EmbeddedDocumentField(
        ConfirmOrderRequest)
    confirm_order_response = mongo_db.EmbeddedDocumentField(
        ConfirmOrderResponse)
    cancel_order_request = mongo_db.EmbeddedDocumentField(
        CancelOrderRequest)
    cancel_order_response = mongo_db.EmbeddedDocumentField(
        CancelOrderResponse)
    release_profile_request = mongo_db.EmbeddedDocumentField(
        ReleaseProfileRequest)
    release_profile_response = mongo_db.EmbeddedDocumentField(
        ReleaseProfileResponse)


class DownloadProgressNotifications(mongo_db.DynamicDocument):
    meta = {'collection': 'download_progress_notifications'}
    status = mongo_db.StringField(default=NotificationStatus.READY, choices=notification_statuses)
    progress_info = mongo_db.DictField(required=True)
    tenant_name = mongo_db.StringField(required=True)
