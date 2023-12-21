from typing import Dict
from .location_local_constants import LocationLocalConstants
from circles_local_database_python.generic_crud import GenericCRUD  # noqa: E402
from circles_local_database_python.generic_crud_ml import GenericCRUDML  # noqa: E402
from circles_local_database_python.connector import Connector   # noqa: E402
from logger_local.Logger import Logger  # noqa: E402


logger = Logger.create_logger(object=LocationLocalConstants.OBJECT_FOR_LOGGER_CODE)


class Neighborhood(GenericCRUD, GenericCRUDML):
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
            neighborhood: str, lang_code: str, title_approved: bool = False, city_id: int = None) -> int:
        logger.start(object={'coordinate': coordinate, 'neighborhood': neighborhood,
                     'lang_code': lang_code, 'title_approved': title_approved, 'city_id': city_id})
        insert_neighborhood_sql = "INSERT INTO neighborhood_table (coordinate) VALUES (POINT(%s, %s))"
        self.cursor.execute(
            insert_neighborhood_sql, (coordinate["latitude"], coordinate["longitude"]))
        neighborhood_id = self.cursor.lastrowid()
        insert_neighborhood_ml_sql = "INSERT INTO neighborhood_ml_table (neighborhood_id, lang_code," \
            " title, title_approved) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(insert_neighborhood_ml_sql, (neighborhood_id,
                            lang_code, neighborhood, title_approved))
        self.connector.commit()
        logger.end(object={'neighborhood_id': neighborhood_id})
        return neighborhood_id

    def get_neighborhood_ids_by_neighborhood_name(self, neighborhood_name: str, city_id: int = None) -> list[int]:
        logger.start(object={'neighborhood_name': neighborhood_name, 'city_id': city_id})

        neighborhood_ids_dicts_list = self.select_multi_dict_by_where_with_none_option(
            view_table_name="neighborhood_ml_view",
            select_clause_value="neighborhood_id",
            condition_column_name="title",
            condition_column_value=neighborhood_name
        )

        # change dicts to ints
        neighborhood_ids = []
        for neighborhood_id_dict in neighborhood_ids_dicts_list:
            neighborhood_ids.append(neighborhood_id_dict["neighborhood_id"])

        logger.end(object={'neighborhood_ids': neighborhood_ids})
        return neighborhood_ids
