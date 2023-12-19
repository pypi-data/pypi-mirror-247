from location_local.location_local_constants import LocationLocalConstants
from data_source_local.src.data_source_enum import DataSource
from entity_type.entity_enum import EntityType
from search_reddit import Reddit
from ProfileRedditConstants import (
    PROFILE_REDDIT_LOCAL_PYTHON_PACKAGE_COMPONENT_ID,
    PROFILE_REDDIT_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME
)
from logger_local.LoggerComponentEnum import LoggerComponentEnum
import json
from circles_importer.importer import Importer as importer

from dotenv import load_dotenv
import sys
import os
sys.path.append(sys.path.append(os.getcwd()))
load_dotenv()
from logger_local.Logger import Logger  # noqa: E402
from user_context_remote.user_context import UserContext  # noqa: E402
from profile_local.comprehensive_profile import ComprehensiveProfilesLocal  # noqa: E402

BRAND_NAME = os.environ.get('BRAND_NAME')
ENVIRONMENT_NAME = os.environ.get('ENVIRONMENT_NAME')

object_to_insert = {
    'component_id': PROFILE_REDDIT_LOCAL_PYTHON_PACKAGE_COMPONENT_ID,
    'component_name': PROFILE_REDDIT_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': 'yoav.e@circ.zone'
}

logger = Logger.create_logger(object=object_to_insert)

user_context = UserContext.login_using_user_identification_and_password()


if BRAND_NAME != 'Circlez':
    logger.exception("please add BRAND_NAME to be Circlez to .env")
    raise

if ENVIRONMENT_NAME is None:
    logger.exception("please add ENVIRONMENT_NAME to .env")
    raise


class RedditImporter:
    def __init__(self):
        pass

    def handle(self, event: dict = None) -> None:
        """
        purpose:
            collect data on reddit users for a certain subreddit
        args:
            event: None for manual input(terminal),
            or a json formatted as such:
            {
                    "subreddit_name": "subreddit_name",
                    "user_count": "user_count"
            }

        example:
            main({"subreddit_name": "python", "user_count": 10})
            saves 10 users that commented on the python subreddit
            to the database

            main(None) asks for user input for subreddit name and user count
        """

        HANDLE_METHOD_NAME = "handle()"
        logger.start(HANDLE_METHOD_NAME, object={"event": event})

        # collect the subreddit name and user count
        reddit = Reddit()
        subreddit_name, user_count = reddit.get_subreddit_and_query(event)
        subreddit = reddit.reddit.subreddit(subreddit_name)

        ##########################################################################
        # Here we need to add the subreddit to the groups table in the database,
        # so we can later add the users to the users table with the group name
        # as a foreign key
        ##########################################################################

        reddit_users = reddit.get_users_from_subreddit(subreddit, user_count)

        # add a new group with the name of the subreddit, if DNE

        # try to fetch the group by name from the DB
        # if DNE, create a new group with the name of the subreddit
        # and send a event to insert it, else, do nothing

        # group_id = get_group_by_name(subreddit_name) // pseudo code
        if reddit_users:
            for reddit_user in reddit_users:

                # this step is inserting the user to the database
                # this needs to return the profile_id for us to be able to use the importer

                profile_id = ComprehensiveProfilesLocal.insert(json.dumps(reddit_user),
                                                               user_context.get_effective_profile_preferred_lang_code())

                # insert to group profile the profile-id and the group-id
                # insert_to_group_profile(profile_id, group_id) // pseudo code

                # register in importer

                importer_obj = importer()
                importer_obj.insert(
                    data_source_id=DataSource.REDDIT_DATA_SOURCE_ID.value,
                    # TODO: uncomment the next line when location_local is fixed https://github.com/circles-zone/location-local-python-package
                    # location_id=LocationLocalConstants.UNKNOWN_LOCATION_ID,
                    location_id=0,
                    entity_type_id=EntityType.PERSONAL_PROFILE_ENTITY_TYPE_ID.value,
                    entity_id=profile_id,
                    url=f"https://www.reddit.com/r/{subreddit_name}",
                    user_id=0
                )

        else:
            logger.error("error no Reddit users found")

        logger.end(HANDLE_METHOD_NAME)
