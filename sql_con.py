from mysql.connector import pooling
from logger import Logger

# Logger setup
logger_mod = Logger("DB")
logger = logger_mod.get_logger()

class ZonixDB():
    def __init__(self, config):
        self.config = config
        self.pool = self._create_pool(config.DB_ADDRESS,
            config.DB_PORT,
            config.DB_SCHEMA,
            config.DB_USERNAME,
            config.DB_PASSWORD,
            config.POOL_SIZE)
 
    def _create_pool(self, host, port, database, user, password, size):
        try:
            pool = pooling.MySQLConnectionPool(pool_name="zrr_pool",
                pool_size=int(size),
                pool_reset_session=True,
                host=host,
                port=port,
                database=database,
                user=user,
                password=password)
            
            logger.info("DB Pool Created")
            return pool

        except Exception as e:
            logger.warning(e)
            logger.warning("DB Pool Failed")
            return None
    
    def dbcon_manager(self, sql:str, get_all=False):
        connection_object = self.pool.get_connection()
        row = None
        try:
            with connection_object.cursor(dictionary=True) as cursor:
                cursor.execute(sql)
                row = cursor.fetchall() if get_all else cursor.fetchone()
                connection_object.commit()
        except Exception as e:
            logger.warning(sql)
            logger.warning(e)
        finally:
            connection_object.close()
        if not row:
            return None
        return row
    
    def update_invitation_number_by_code(self, invite_code):
        sql = f"""UPDATE invitation_table
        set invited_number = invited_number + 1
        where invitation_code = '{invite_code}'"""
        return self.dbcon_manager(sql)