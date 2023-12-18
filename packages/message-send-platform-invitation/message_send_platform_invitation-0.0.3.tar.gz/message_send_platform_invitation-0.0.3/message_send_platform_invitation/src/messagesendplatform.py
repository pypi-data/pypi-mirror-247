"""imports"""
from typing import List

from circles_local_database_python.connector import Connector
from circles_local_database_python.generic_crud import GenericCRUD
from dotenv import load_dotenv
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from message_local.Recipient import Recipient
from messages_local.MessagesLocal import MessagesLocal

MESSAGE_SEND_PLATFORM_INVITATION_LOCAL_PYTHON_COMPONENT_ID = 243
MESSAGE_SEND_PLATFORM_INVITATION_LOCAL_PYTHON_COMPONENT_COMPONENT_NAME = "message-send-platform-invitation-local-python"
DEVELOPER_EMAIL = 'jenya.b@circ.zone'
object1 = {
    'component_id': MESSAGE_SEND_PLATFORM_INVITATION_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': MESSAGE_SEND_PLATFORM_INVITATION_LOCAL_PYTHON_COMPONENT_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
}
logger = Logger.create_logger(object=object1)

load_dotenv()


class MessageSendPlatform(GenericCRUD):
    """Message send platform class"""

    def __init__(self, schema_name="message", connection: Connector = None) -> None:
        super().__init__(schema_name, connection)

    def _get_potential_person_list_by_campaign_id(self, campaign_id: int, limit: int = 100) -> List[Recipient]:
        """return list of person id """
        logger.start(f"get potential person list by campaign id={campaign_id}")
        query = (
            "SELECT criteria_table.min_age, criteria_table.max_age "
            "FROM campaign.campaign_table AS campaign_table "
            "JOIN criteria.criteria_table AS criteria_table "
            "ON criteria_table.criteria_id = campaign_table.criteria_id "
            "WHERE campaign_table.campaign_id = %s LIMIT 1"
        )
        self.cursor.execute(query, (campaign_id,))
        result = self.cursor.fetchone()
        if result is None:
            logger.end(f"campaign_id={campaign_id} not found")
            return []
        min_age, max_age = result
        where = "TRUE"
        if min_age is not None:
            where += f" AND TIMESTAMPDIFF(YEAR, person_birthday_date, CURDATE()) >= {min_age}"
        if max_age is not None:
            where += f" AND TIMESTAMPDIFF(YEAR, person_birthday_date, CURDATE()) <= {max_age}"
        query2 = (
                "SELECT DISTINCT user_id, person_id, user_main_email, profile_id, "
                "   profile_phone_full_number_normalized, profile_preferred_lang_code"
                " FROM user.user_general_view " + (
                    "WHERE " + where if where else "") + f" LIMIT {limit}"
        )
        self.cursor.execute(query2)
        result = self.cursor.fetchall()
        result = [Recipient(user_id=x[0], person_id=x[1], email_address=x[2],
                            profile_id=x[3], telephone_number=x[4], preferred_language=x[5])
                  for x in result]

        """
        old_query = (
            "SELECT profile.profile_table.profile_id "
            "FROM person.person_table AS person_table "
            "JOIN criteria.criteria_table AS criteria_table "
            "ON TIMESTAMPDIFF(YEAR, person_table.birthday_date, CURDATE()) >= criteria_table.min_age "
            "AND TIMESTAMPDIFF(YEAR, person_table.birthday_date, CURDATE()) <= criteria_table.max_age "
            "AND person.person_table.gender_id = criteria_table.gender_list_id "
            "AND person.person_table.location_id = criteria_table.location_id "
            "JOIN campaign.campaign_table AS campaign_table "
            "ON campaign_table.criteria_id = criteria_table.criteria_id "
            "JOIN profile.profile_table AS profile_table "
            "ON profile_table.person_id = person_table.person_id "
            "JOIN person.person_kid_table AS person_kid_table "
            "ON person_kid_table.person_id = person_table.person_id "
            "AND person_kid_table.number_of_kids >= criteria_table.min_number_of_kids "
            "AND person_kid_table.number_of_kids <= criteria_table.max_number_of_kids "
            f"WHERE campaign_table.campaign_id = {campaign_id} LIMIT {limit}"
        )"""
        logger.end(f"potential person list by campaign id={campaign_id}",
                   object={"Results": [str(x) for x in result]})
        return result

    def _get_number_of_invitations_sent_in_the_last_24_hours(self, campaign_id: int) -> int:
        """return number of invitations"""
        logger.start(
            f"get number of invitations sent in the last 24_hours for campaign id={campaign_id}")
        query = (
            "SELECT COUNT(*) FROM message_outbox_view WHERE campaign_id ="
            f"{campaign_id} AND return_code=0 AND updated_timestamp - INTERVAL 24 HOUR"
        )
        self.schema_name = "message"
        self.cursor.execute(query)
        number_of_invitations_tuple = self.cursor.fetchall()
        number_of_invitation = number_of_invitations_tuple[0][0]
        logger.end(f"number_of_invitations={number_of_invitation}")
        return number_of_invitation

    def _get_number_of_invitations_to_send(self, campaign_id, multiplier: float = 1, additional_invitations: int = 0) -> int:
        """get number to send after multiplier"""
        logger.start()
        invitations_sent_in_the_last_24_hours = int(self._get_number_of_invitations_sent_in_the_last_24_hours(
            campaign_id) * multiplier + additional_invitations)
        logger.end(
            f"number_of_invitations_to_send={invitations_sent_in_the_last_24_hours}")
        logger.info(
            f"number of invitations to sends={invitations_sent_in_the_last_24_hours}")
        return invitations_sent_in_the_last_24_hours

    def send_message(self, campaign_id: int) -> None:
        count = self._get_number_of_invitations_to_send(campaign_id, multiplier=0.1, additional_invitations=20)
        list_persons = self._get_potential_person_list_by_campaign_id(campaign_id, count)
        query = (
            "SELECT campaign_table.message_template_id, message_template_ml_table.sms_body_template"
            "FROM campaign.campaign_table JOIN message_template.message_template_ml_table"
            "ON campaign_table.message_template_id = message_template_ml_table.message_template_id"
            f"WHERE campaign_table.campaign_id = {campaign_id}"
        )
        self.cursor.execute(query)
        text_template = self.cursor.fetchall()
        MessagesLocal().send_scheduled(to_recipients=list_persons, original_body=text_template,
                                       campaign_id=campaign_id)

    def send(self) -> None:
        self.cursor.execute("SELECT campaign_id FROM campaign.campaign_table WHERE NOW() >= start_timestamp "
                            "AND (end_timestamp IS NULL OR NOW() <= end_timestamp)")
        campaigns = self.cursor.fetchall()
        for campaign in campaigns:
            self.send_message(campaign[0])


if __name__ == '__main__':
    print(MessageSendPlatform("profile")._get_potential_person_list_by_campaign_id(1, 10))
    # print(MessageSendPlatform("message").get_number_of_invitations_sent_in_the_last_24_hours(1))
    # print(MessageSendPlatform("message").get_number_of_invitations_to_send(1))
