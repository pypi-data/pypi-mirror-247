from sdk.src.utilities import create_http_headers
from .event_remote_util import EventRemoteUtil
from url_local.url_circlez import OurUrl
from url_local.action_name_enum import ActionName
from url_local.entity_name_enum import EntityName
from url_local.component_name_enum import ComponentName
from logger_local.Logger import Logger
from .event_constants import EventRemoteConstants
import copy
import requests
import os
import sys
from dotenv import load_dotenv
from event_external_local.external_event_local_class import ExternalEventsLocal
load_dotenv()
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_directory, '..'))


BRAND_NAME = os.getenv("BRAND_NAME")
ENVIRONMENT_NAME = os.getenv("ENVIRONMENT_NAME")
EVENT_API_VERSION = 1


class EventRemote:

    def __init__(self):
        self.event_external_local = ExternalEventsLocal()
        self.url_circlez = OurUrl()
        self.logger = Logger.create_logger(
            object=EventRemoteConstants.EVENT_REMOTE_CODE_LOGGER_OBJECT)
        self.brand_name = BRAND_NAME
        self.env_name = ENVIRONMENT_NAME

    def get_url_by_action_name(self, action_name: ActionName,
                               path_parameters: dict = None):
        # optional query_parameters can be added if needed
        return self.url_circlez.endpoint_url(
            brand_name=self.brand_name,
            environment_name=self.env_name,
            component_name=ComponentName.EVENT.value,
            entity_name=EntityName.EVENT.value,
            version=EVENT_API_VERSION,
            action_name=action_name.value,
            path_parameters=path_parameters if path_parameters else None
        )

    def create(self, location_id: int, organizers_profile_id: int,
               website_url: str, facebook_event_url: str = '',
               meetup_event_url: str = '', registration_url: str = ''):
        event_payload_json = {
            'location_id': location_id,
            'organizers_profile_id': organizers_profile_id,
            'website_url': website_url,
            'facebook_event_url': facebook_event_url,
            'meetup_event_url': meetup_event_url,
            'registration_url': registration_url
        }
        object_start = copy.copy(event_payload_json)
        self.logger.start("Start create event", object=object_start)
        try:
            url = self.get_url_by_action_name(ActionName.CREATE_EVENT)

            self.logger.info(
                "Endpoint event  - createEvent action: " + url)

            headers = create_http_headers(
                self.logger.user_context.get_user_JWT())
            response = requests.post(
                url=url, json=event_payload_json, headers=headers)
            self.logger.end(
                f"End create event-remote, response: {str(response)}")
            return response

        except requests.ConnectionError as e:
            self.logger.exception(
                "Network problem (e.g. failed to connect)", object=e)
            self.logger.end("End create event-remote, connection error exception")  # noqa
            raise

        except requests.Timeout as e:
            self.logger.exception("Request timed out", e)
            self.logger.end("End create event-remote, timeout exception")  # noqa
            raise

        except requests.RequestException as e:
            self.logger.exception(f"General error: {str(e)}", object=e)
            self.logger.end("End create event-remote, request exception")  # noqa
            raise

        except Exception as e:
            self.logger.exception(
                f"An unexpected error occurred: {str(e)}", object=e)
            self.logger.end("End create event-remote, general exception")  # noqa
            raise

    def create_external_event(self, external_event_details: dict):
        external_event = {
            'external_event_details': external_event_details
        }
        self.logger.start("Start create external event",
                          object=external_event)
        try:
            url = self.get_url_by_action_name(ActionName.CREATE_EVENT)

            self.logger.info(
                "Endpoint event  - createEvent action: " + url)

            headers = create_http_headers(
                self.logger.user_context.get_user_JWT())
            event_payload_json = EventRemoteUtil.create_event_from_external_event(external_event=external_event_details)  # noqa
            event_response = requests.post(url=url,
                                           json=event_payload_json,
                                           headers=headers)

            event_id = event_response.json().get('event_id')

            external_event_id = self.event_external_local.insert(system_id=external_event_details.get('system_id'),  # noqa
                                                                 subsystem_id=external_event_details.get('subsystem_id', None),  # noqa
                                                                 url=external_event_details.get('url'),  # noqa
                                                                 external_event_identifier=external_event_details.get('external_event_identifier'),  # noqa
                                                                 environment_id=external_event_details.get('environment_id', 1))  # noqa
            event_ids = {
                'event_id': event_id,
                'external_event_id': external_event_id
            }
            object_end = copy.copy(event_ids)
            self.logger.end("End create external event-remote",
                            object=object_end)
            return event_ids

        except requests.ConnectionError as e:
            self.logger.exception(
                "Network problem (e.g. failed to connect)", object=e)
            self.logger.end("End create external event-remote connection error exception")  # noqa
            raise

        except requests.Timeout as e:
            self.logger.exception("Request timed out", e)
            self.logger.end("End create external event-remote timeout exception")  # noqa
            raise

        except requests.RequestException as e:
            self.logger.exception(f"General error: {str(e)}", object=e)
            self.logger.end("End create external event-remote request exception")  # noqa
            raise

        except Exception as e:
            self.logger.exception(
                f"An unexpected error occurred: {str(e)}", object=e)
            self.logger.end("End create external event-remote general exception")  # noqa
            raise

    def create_external_events(self, external_events_details: list):
        external_events = {
            'external_events_details': external_events_details
        }
        self.logger.start("Start create external events",
                          object=external_events)
        try:
            url = self.get_url_by_action_name(ActionName.CREATE_EVENT)

            self.logger.info(
                "Endpoint event  - createEvent action: " + url)
            events_ids = []

            for external_event in external_events_details:
                events_ids.append(self.create_external_event(external_event_details=external_event))  # noqa

            object_end = {
                'events_ids': events_ids
            }
            self.logger.end("End create external events-remote",
                            object=object_end)
            return events_ids

        except requests.ConnectionError as e:
            self.logger.exception(
                "Network problem (e.g. failed to connect)", object=e)
            self.logger.end("End create external events-remote connection error exception")  # noqa
            raise

        except requests.Timeout as e:
            self.logger.exception("Request timed out", e)
            self.logger.end("End create external events-remote timeout exception")  # noqa
            raise

        except requests.RequestException as e:
            self.logger.exception(f"General error: {str(e)}", object=e)
            self.logger.end("End create external events-remote request exception")  # noqa
            raise

        except Exception as e:
            self.logger.exception(
                f"An unexpected error occurred: {str(e)}", object=e)
            self.logger.end("End create external events-remote general exception")  # noqa
            raise

    def get_event_by_event_id(self, event_id: int):
        path_parameters = {
            'event_id': event_id
        }
        self.logger.start("Start get event-remote", object=path_parameters)
        try:
            url = self.get_url_by_action_name(
                ActionName.GET_EVENT_BY_ID, path_parameters=path_parameters)

            self.logger.info(
                "Endpoint event - getEventById action: " + url)

            headers = create_http_headers(
                self.logger.user_context.get_user_JWT())
            response = requests.get(url=url, headers=headers)
            self.logger.end(
                f"End get event-remote, response: {str(response)}")
            return response

        except requests.ConnectionError as e:
            self.logger.exception(
                "Network problem (e.g. failed to connect)", object=e)
            self.logger.end("End get event-remote connection error exception")
            raise

        except requests.Timeout as e:
            self.logger.exception("Request timed out", e)
            self.logger.end("End get event-remote timeout exception")
            raise

        except requests.RequestException as e:
            self.logger.exception(f"General error: {str(e)}", object=e)
            self.logger.end("End get event-remote request exception")
            raise

        except Exception as e:
            self.logger.exception(
                f"An unexpected error occurred: {str(e)}", object=e)
            self.logger.end("End get event-remote general exception")
            raise

    def delete_event_by_id(self, event_id: int):
        path_parameters = {
            'event_id': event_id
        }
        self.logger.start("Start delete event-remote", object=path_parameters)
        try:
            url = self.get_url_by_action_name(
                ActionName.DELETE_EVENT_BY_ID, path_parameters=path_parameters)

            self.logger.info(
                "Endpoint event - deleteEventById action: " + url)

            headers = create_http_headers(
                self.logger.user_context.get_user_JWT())

            response = requests.delete(url=url, headers=headers)
            self.logger.end(
                f"End delete event-remote, response: {str(response)}")
            return response

        except requests.ConnectionError as e:
            self.logger.exception(
                "Network problem (e.g. failed to connect)", object=e)
            self.logger.end("End delete event-remote connection error exception")  # noqa
            raise

        except requests.Timeout as e:
            self.logger.exception("Request timed out", e)
            self.logger.end("End delete event-remote timeout exception")
            raise

        except requests.RequestException as e:
            self.logger.exception(f"General error: {str(e)}", object=e)
            self.logger.end("End delete event-remote request exception")
            raise

        except Exception as e:
            self.logger.exception(
                f"An unexpected error occurred: {str(e)}", object=e)
            self.logger.end("End delete event-remote general exception")
            raise

    def update_event_by_id(self, event_id: int, location_id: int,
                           organizers_profile_id: int, website_url: str,
                           facebook_event_url: str = '',
                           meetup_event_url: str = '',
                           registration_url: str = ''):

        object_start = {
            'event_id': event_id,
            'location_id': location_id,
            'organizers_profile_id': organizers_profile_id,
            'website_url': website_url,
            'facebook_event_url': facebook_event_url,
            'meetup_event_url': meetup_event_url,
            'registration_url': registration_url
        }
        self.logger.start("Start update event-remote", object=object_start)
        try:
            path_parameters = {
                'event_id': event_id
            }
            url = self.get_url_by_action_name(
                ActionName.UPDATE_EVENT_BY_ID, path_parameters=path_parameters)

            event_payload_json = {
                "location_id": location_id,
                "organizers_profile_id": organizers_profile_id,
                "website_url": website_url,
                "facebook_event_url": facebook_event_url,
                "meetup_event_url": meetup_event_url,
                "registration_url": registration_url
            }

            self.logger.info(
                "Endpoint event - updateEventById action: " + url)

            headers = create_http_headers(
                self.logger.user_context.get_user_JWT())

            response = requests.put(
                url=url, json=event_payload_json, headers=headers)
            self.logger.end(
                f"End update event-remote, response: {str(response)}")
            return response

        except requests.ConnectionError as e:
            self.logger.exception(
                "Network problem (e.g. failed to connect)", object=e)
            self.logger.end("End update event-remote connection error exception")  # noqa
            raise

        except requests.Timeout as e:
            self.logger.exception("Request timed out", e)
            self.logger.end("End update event-remote timeout exception")
            raise

        except requests.RequestException as e:
            self.logger.exception(f"General error: {str(e)}", object=e)
            self.logger.end("End update event-remote request exception")
            raise

        except Exception as e:
            self.logger.exception(
                f"An unexpected error occurred: {str(e)}", object=e)
            self.logger.end("End update event-remote general exception")
            raise
