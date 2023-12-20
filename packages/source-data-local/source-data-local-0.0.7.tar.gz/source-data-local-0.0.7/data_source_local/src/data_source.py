from dotenv import load_dotenv
load_dotenv()
from circles_local_database_python.generic_crud import GenericCRUD  # noqa: E402, E501
from language_local.lang_code import LangCode  # noqa: E402
from logger_local.Logger import Logger  # noqa: E402
from .data_source_constans import obj  # noqa: E402


logger = Logger.create_logger(object=obj)


class DataSource(GenericCRUD):

    def __init__(self):
        super().__init__(default_schema_name='data_source',
                         default_table_name='data_source_table',
                         default_view_table_name='data_source_ml_en_view')  # noqa: E501

    def insert_data_source(self, data_source_name: str, lang_code: str = LangCode.ENGLISH.value) -> int:  # noqa: E501
        METHOD_NAME = 'insert_source_data'
        logger.start(METHOD_NAME, object={
                     'data_source_name': data_source_name,
                     'lang_code': lang_code})
        try:
            data_source_json = {
                'created_user_id': logger.user_context.get_real_user_id(),
                'updated_user_id': logger.user_context.get_effective_user_id()
            }
            data_source_id = self.insert(data_json=data_source_json)
            data_source_ml_json = {
                'data_source_id': data_source_id,
                'lang_code': lang_code,
                'data_source_name': data_source_name,
                'created_user_id': logger.user_context.get_real_user_id(),
                'updated_user_id': logger.user_context.get_effective_user_id()
            }
            data_source_ml_id = self.insert(
                table_name='data_source_ml_table',
                data_json=data_source_ml_json)
            logger.end(METHOD_NAME, object={
                       'data_source_id': data_source_id,
                       'data_source_ml_id': data_source_ml_id})
            return data_source_id, data_source_ml_id

        except Exception as e:
            logger.exception(
                log_message="faild to insert data_source " + METHOD_NAME + str(e), object=e)  # noqa: E501
            logger.end(METHOD_NAME, object={
                       'data_source_name': data_source_name, 'lang_code': lang_code})  # noqa: E501
            raise e

    def get_data_source_id_by_name(self, data_source_name: str) -> int:
        METHOD_NAME = 'get_data_source_id_by_name'
        try:
            logger.start(log_message=METHOD_NAME, object={
                         'data_source_name': data_source_name})
            data_source_id = self.select_one_tuple_by_id(
                select_clause_value='data_source_id',
                id_column_name='data_source_name',
                id_column_value=data_source_name)
            if data_source_id:
                logger.end(METHOD_NAME, object={
                           'data_source_id': data_source_id})
                return data_source_id
            else:
                logger.end(METHOD_NAME, object={
                           'data_source_id': data_source_id})
                return None
        except Exception as e:
            logger.exception(
                log_message="faild to get data_source_id " + METHOD_NAME + str(e), object=e)  # noqa: E501
            logger.end(METHOD_NAME, object={
                       'data_source_name': data_source_name})
            raise e

    def get_data_source_name_by_id(self, data_source_id: int) -> str:
        METHOD_NAME = 'get_data_source_name_by_id'
        try:
            logger.start(log_message=METHOD_NAME, object={
                         'data_source_id': data_source_id})
            data_source_name = self.select_one_tuple_by_id(
                select_clause_value='data_source_name',
                id_column_name='data_source_id',
                id_column_value=data_source_id)
            if data_source_name:
                logger.end(METHOD_NAME, object={
                           'data_source_name': data_source_name})
                return data_source_name
            else:
                logger.end(METHOD_NAME, object={
                           'data_source_name': data_source_name})
                return None
        except Exception as e:
            logger.exception(
                log_message="faild to get data_source_name " + METHOD_NAME + str(e), object=e)  # noqa: E501
            logger.end(METHOD_NAME, object={'data_source_id': data_source_id})
            raise e
