from typing import Dict
from .location_local_constants import LocationLocalConstants
from circles_local_database_python.generic_crud import GenericCRUD  # noqa: E402
from circles_local_database_python.generic_crud_ml import GenericCRUDML  # noqa: E402
from circles_local_database_python.connector import Connector   # noqa: E402
from logger_local.Logger import Logger  # noqa: E402


logger = Logger.create_logger(object=LocationLocalConstants.OBJECT_FOR_LOGGER_CODE)


class State(GenericCRUD, GenericCRUDML):
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
            state: str, lang_code: str, state_name_approved: bool = False, country_id: int = None) -> int:
        logger.start(object={'coordinate': coordinate, 'state': state,
                     'lang_code': lang_code, 'state_name_approved': state_name_approved, 'country_id': country_id})
        insert_state_sql = "INSERT INTO state_table (coordinate) VALUES (POINT(%s, %s))"
        self.cursor.execute(
            insert_state_sql, (coordinate["latitude"], coordinate["longitude"]))
        state_id = self.cursor.lastrowid()
        insert_state_ml_sql = "INSERT INTO state_ml_table (state_id, lang_code, state_name," \
            " state_name_approved) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(
            insert_state_ml_sql, (state_id, lang_code, state, state_name_approved))
        self.connector.commit()
        logger.end(object={'state_id': state_id})
        return state_id

    def get_state_ids_by_state_name(self, state_name: str, country_id: int = None) -> list[int]:
        logger.start(object={'state_name': state_name, 'country_id': country_id})

        state_ids_dicts_list = self.select_multi_dict_by_where_with_none_option(
            view_table_name="state_ml_view",
            select_clause_value="state_id",
            condition_column_name="state_name",
            condition_column_value=state_name
        )

        # change dicts to ints
        state_ids = []
        for state_id_dict in state_ids_dicts_list:
            state_ids.append(state_id_dict["state_id"])

        logger.end(object={'state_ids': state_ids})
        return state_ids
