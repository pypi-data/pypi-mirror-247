from typing import Dict
from .location_local_constants import LocationLocalConstants
from circles_local_database_python.generic_crud import GenericCRUD  # noqa: E402
from circles_local_database_python.generic_crud_ml import GenericCRUDML  # noqa: E402
from circles_local_database_python.connector import Connector   # noqa: E402
from logger_local.Logger import Logger  # noqa: E402


logger = Logger.create_logger(object=LocationLocalConstants.OBJECT_FOR_LOGGER_CODE)


class County(GenericCRUD, GenericCRUDML):
    def __init__(self):
        logger.start()

        super().__init__(default_schema_name="location")

        # TODO: use GenericCRUD and GenericCRUDML and delete the following 2 lines
        self.connector = Connector.connect("location")
        self.cursor = self.connector.cursor()

        logger.end()

    # TODO: use GenericCRUD's and GenericCRUDML's insert methods
    def insert(
            self, coordinate: Dict[str, float],
            county: str, lang_code: str, title_approved: bool = False, state_id: int = None) -> int:
        logger.start(object={'coordinate': coordinate, 'county': county,
                     'lang_code': lang_code, 'title_approved': title_approved, 'state_id': state_id})
        insert_county_sql = "INSERT INTO county_table (coordinate) VALUES (POINT(%s, %s))"
        self.cursor.execute(
            insert_county_sql, (coordinate["latitude"], coordinate["longitude"]))
        county_id = self.cursor.lastrowid()
        insert_county_ml_sql = "INSERT INTO county_ml_table (county_id, lang_code," \
            " title, title_approved) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(insert_county_ml_sql, (county_id,
                            lang_code, county, title_approved))
        self.connector.commit()
        logger.end(object={'county_id': county_id})
        return county_id

    # TODO: uncomment the commented lines after we add state_id to county_ml_table and county_ml_view
    def get_county_ids_by_county_name_state_id(self, county_name: str, state_id: int = None) -> list[int]:
        logger.start(object={'county_name': county_name, 'state_id': state_id})

        county_ids_dicts_list = self.select_multi_dict_by_where_with_none_option(
            view_table_name=LocationLocalConstants.COUNTY_ML_VIEW_NAME,
            # select_clause_value="county_id, state_id",
            select_clause_value="county_id",
            condition_column_name="title",
            condition_column_value=county_name
        )
        # filtered_county_ids by state_id
        '''
        filtered_county_ids = []
        for county_id in county_ids:
            if county_id["state_id"] == state_id:
                filtered_county_ids.append(county_id["county_id"])

        logger.end(object={'county_ids': county_ids})
        return filtered_county_ids
        '''
        # change dicts to ints
        county_ids = []
        for county_id_dict in county_ids_dicts_list:
            county_ids.append(county_id_dict["county_id"])
        return county_ids
