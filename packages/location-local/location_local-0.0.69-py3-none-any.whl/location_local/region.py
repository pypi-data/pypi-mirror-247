from typing import Dict
from .location_local_constants import LocationLocalConstants
from circles_local_database_python.generic_crud import GenericCRUD  # noqa: E402
from circles_local_database_python.generic_crud_ml import GenericCRUDML  # noqa: E402
from circles_local_database_python.connector import Connector   # noqa: E402
from logger_local.Logger import Logger  # noqa: E402

logger = Logger.create_logger(object=LocationLocalConstants.OBJECT_FOR_LOGGER_CODE)


class Region(GenericCRUD, GenericCRUDML):
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
            region: str, lang_code: str, title_approved: bool = False, country_id: int = None) -> int:
        logger.start(object={'coordinate': coordinate, 'region': region,
                     'lang_code': lang_code, 'title_approved': title_approved, 'country_id': country_id})
        insert_region_sql = "INSERT INTO region_table (coordinate) VALUES (POINT(%s, %s))"
        self.cursor.execute(
            insert_region_sql, (coordinate["latitude"], coordinate["longitude"]))
        region_id = self.cursor.lastrowid()
        insert_region_ml_sql = "INSERT INTO region_ml_table (region_id, lang_code, title, title_approved)" \
            " VALUES (%s, %s, %s, %s)"
        self.cursor.execute(insert_region_ml_sql, (region_id,
                            lang_code, region, title_approved))
        self.connector.commit()
        logger.end(object={'region_id': region_id})
        return region_id

    def get_region_ids_by_region_name(self, region_name: str, country_id: int = None) -> list[int]:
        logger.start(object={'region_name': region_name, 'country_id': country_id})

        region_ids_dicts_list = self.select_multi_dict_by_where_with_none_option(
            view_table_name="region_ml_view",
            select_clause_value="region_id",
            condition_column_name="title",
            condition_column_value=region_name
        )

        # change dicts to ints
        region_ids = []
        for region_id_dict in region_ids_dicts_list:
            region_ids.append(region_id_dict["region_id"])

        logger.end(object={'region_ids': region_ids})
        return region_ids

