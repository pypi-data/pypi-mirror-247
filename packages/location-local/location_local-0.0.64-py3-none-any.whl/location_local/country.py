import os
from typing import Dict
from opencage.geocoder import OpenCageGeocode
try:
    # When running from this package
    from location_local_constants import LocationLocalConstants
except Exception:
    # When importing this module from another package
    from location_local.location_local_constants import LocationLocalConstants
from dotenv import load_dotenv
load_dotenv()
from circles_local_database_python.generic_crud import GenericCRUD  # noqa: E402
from circles_local_database_python.connector import Connector  # noqa: E402
from logger_local.Logger import Logger  # noqa: E402
from language_local.lang_code import LangCode  # noqa: E402
api_key = os.getenv("OPENCAGE_KEY")

logger = Logger.create_logger(object=LocationLocalConstants.OBJECT_FOR_LOGGER_CODE)


class Country(GenericCRUD):
    def __init__(self):
        logger.start()

        self.connector = Connector.connect("location")
        self.cursor = self.connector.cursor()

        logger.end()

    def insert(self, coordinate: Dict[str, float],
                       country: str, lang_code: LangCode, title_approved: bool = False,
                       new_country_data: Dict[str, any] = None) -> int:
        logger.start(object={'coordinate': coordinate, 'country': country, 'lang_code': lang_code,
                     'title_approved': title_approved, 'new_country_data': new_country_data})
        try:
            insert_country_sql = "INSERT INTO country_table (coordinate, iso, `name`, nicename, iso3, numcode, phonecode) VALUES (POINT(%s, %s), %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(
                insert_country_sql,
                (coordinate["latitude"],
                 coordinate["longitude"],
                 new_country_data["iso"],
                 new_country_data["name"],
                 new_country_data["nicename"],
                 new_country_data["iso3"],
                 new_country_data["numcode"],
                 new_country_data["phonecode"]))
        except Exception as e:
            logger.exception("error in insert country", e)
            logger.end()
            raise e
        try:
            country_id = self.cursor.lastrowid()
            insert_country_ml_sql = "INSERT INTO country_ml_table (country_id, lang_code, title," \
                " title_approved) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(insert_country_ml_sql, (country_id,
                                                  lang_code, country, title_approved))
            self.connector.commit()
        except Exception as e:
            logger.exception("error in insert country", e)
            logger.end()
            raise e
        logger.end(object={'country_id': country_id})
        return country_id

    @staticmethod
    def get_country_id_by_country_name(country_name: str) -> int:
        logger.start(object={'country_name': country_name})

        connector = Connector.connect("location")
        cursor = connector.cursor()

        select_country_ml_sql = "SELECT country_id FROM country_ml_view WHERE `name` = %s LIMIT 1"
        cursor.execute(select_country_ml_sql, (country_name,))
        country_id = cursor.fetchone()
        if country_id is not None:
            country_id = country_id[0]

        logger.end(object={'country_id': country_id})
        return country_id

    @staticmethod
    def get_country_name(location):
        # Create a geocoder instance
        logger.start(object={'location': location})

        # Define the city or state
        geocoder = OpenCageGeocode(api_key)

        # Use geocoding to get the location details
        results = geocoder.geocode(location)

        if results and len(results) > 0:
            first_result = results[0]
            components = first_result['components']

            # Extract the country from components
            country_name = components.get('country', '')
            if not country_name:
                # If country is not found, check for country_code as an alternative
                country_name = components.get('country_code', '')
        else:
            country_name = None
            logger.error("country didnt  found for %s." % location)
        logger.end(object={'country_name': country_name})
        return country_name
