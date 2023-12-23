import pymysql
from .log import log


class ConnectMysql(object):
    instance = None
    init_flag = False

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, host, user, password, port, database):
        if self.init_flag:
            return
        try:
            self.db = pymysql.connect(
                host=host,
                user=user,
                password=password,
                port=port,
                database=database,
                cursorclass=pymysql.cursors.DictCursor,
            )
            self.cursor = self.db.cursor()
            log.debug(f"mysql connect success!")
        except Exception as msg:
            self.cursor = None
            log.error(f"mysql connect error: {msg}")
        self.init_flag = True

    def query_sql(self, sql):
        """查询，返回结果"""
        if self.cursor:
            log.debug(f"query sql: {sql}!")
            try:
                self.cursor.execute(sql)
                result = self.cursor.fetchall()
                self.db.commit()
                if len(result) == 1:
                    result = result[0]
                elif len(result) == 0:
                    result = []
                log.info(f"query result: {result}")
                return result
            except Exception as msg:
                log.error(f"query error: {msg}")

    def execute_sql(self, sql):
        """修改，新增，删除"""
        if self.cursor:
            log.debug(f"execute sql: {sql}")
            try:
                result = self.cursor.execute(sql)
                log.debug(f"execute result: {result}")
                self.db.commit()
                return result
            except Exception as msg:
                log.error(f"execute error: {msg}")

    def close(self):
        if self.cursor:
            self.cursor.close()
            self.db.close()
            log.debug(f"close db!")


def connect_redis(env_obj):
    """
    连接redis
    env_obj: 环境对象
    return: redis 连接对象
    """
    if hasattr(env_obj, 'REDIS'):
        try:
            import redis  # noqa
            redis_obj = redis.StrictRedis(**env_obj.REDIS)  # noqa
            return {
                "redis": redis_obj
            }
        except Exception as msg:
            log.error(f'redis connect init error: {msg}')
            return {
                "redis": None
            }
    else:
        return {
            "redis": lambda x: log.error("REDIS connect error in config.py")
        }