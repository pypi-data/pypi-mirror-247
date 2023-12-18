from logger_local.LoggerComponentEnum import LoggerComponentEnum

MESSAGE_LOCAL_PYTHON_COMPONENT_ID = ""
MESSAGE_LOCAL_PYTHON_COMPONENT_COMPONENT_NAME = ""
DEVELOPER_EMAIL = 'jenya.b@circ.zone'
object_message = {
    'component_id': MESSAGE_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': MESSAGE_LOCAL_PYTHON_COMPONENT_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
}

DEFAULT_HEADERS = {"Content-Type": "application/json"}

TEST_API_TYPE_ID = 4

# PROVIDERS
AWS_SMS_MESSAGE_PROVIDER_ID = 1
INFORU_MESSAGE_PROVIDER_ID = 2
AWS_EMAIL = 4

# SMS
SMS_MESSAGE_LENGTH = 160
UNICODE_SMS_MESSAGE_LENGTH = 70

