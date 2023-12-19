import pyodbc
from .debug_info import debug_info


class SQLHelper:
    @debug_info('DataCore Sync', 'connecting to database')
    def __init__(self, server_name: str, db_name: str):
        driver_names = [x for x in pyodbc.drivers() if x.endswith(' for SQL Server')]
        sql_connection_string = (
            'Driver={' + driver_names[0] + '};'
            'Server=' + server_name + ';'
            'Database=' + db_name + ';'
            'Trusted_Connection=yes;'
            'Integrated Security=SSPI;'
            'Persist Security Info=True;'
            'APP=DataCore Sync/5.0.0, Python, BI CORP;'
        )
        try:
            self.conn = pyodbc.connect(sql_connection_string)

        except pyodbc.Error as ex:
            print('[ERROR] Fatal Error: SQL Server connection can\'t be done. Server: ', server_name)
            print(ex)
            raise SystemError
