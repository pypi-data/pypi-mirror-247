import random
import string

from circles_local_database_python.generic_crud import GenericCRUD
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from message_local.Recipient import Recipient

SMART_LINK_COMPONENT_ID = 258
SMART_LINK_COMPONENT_NAME = "smartlink"
DEVELOPER_EMAIL = "akiva.s@circ.zone"
object1 = {
    'component_id': SMART_LINK_COMPONENT_ID,
    'component_name': SMART_LINK_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
}
logger = Logger.create_logger(object=object1)

SMART_LINK_LENGTH = 20  # (26*2 + 10) ^ 20 = 62^20 possibilities (number with 36 digits)


class SmartLink(GenericCRUD):
    def __init__(self) -> None:
        super().__init__(default_schema_name="smartlink",
                         default_table_name="smartlink_table",
                         default_view_table_name="smartlink_view",
                         default_id_column_name="magic_link_id")

    def _generate_random_string(self, length: int) -> str:
        logger.start()

        letters = string.ascii_letters + string.digits
        result = ''.join(random.choice(letters) for i in range(length))

        logger.end(f"result: {result}")
        return result

    def insert(self, from_recipient: Recipient, to_recipient: Recipient,
               campaign_id: int, action_id: int) -> int:
        logger.start()

        smart_link_id = self._generate_random_string(length=SMART_LINK_LENGTH)
        # smart_link = f"www.circ.zone?a={smart_link_id}"
        data_json = {
            "identification": smart_link_id,
            "campaign_id": campaign_id,
            "action_id": action_id,
            "from_email": from_recipient.get_email_address(),
            "to_email": to_recipient.get_email_address(),
            "from_normalized_phone": from_recipient.get_canonical_telephone(),
            "to_normalized_phone": to_recipient.get_canonical_telephone(),
            "lang_code": to_recipient.get_preferred_language()
            # TODO: get to_group_id and effective user id
        }
        # contact_id, user_id, person_id, profile_id
        data_json.update({"to_" + key: value for key, value in to_recipient.to_json().items()
                          if key.endswith("_id")})
        data_json.update({"from_" + key: value for key, value in from_recipient.to_json().items()
                          if key.endswith("_id")})
        inserted_id = super().insert(data_json=data_json)

        logger.end(f"inserted_id: {inserted_id}")
        return inserted_id
