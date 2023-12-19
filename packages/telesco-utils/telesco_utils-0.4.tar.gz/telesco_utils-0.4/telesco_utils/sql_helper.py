import pyodbc
from .debug_info import debug_info


class SQLHelper:
    conn = None

    @debug_info('DataCore Sync', 'connecting to database')
    def __init__(self, server_name: str, db_name: str, app_name: str = 'python sql helper'):
        driver_names = [x for x in pyodbc.drivers() if x.endswith(' for SQL Server')]
        sql_connection_string = (
            'Driver={' + driver_names[0] + '};'
            'Server=' + server_name + ';'
            'Database=' + db_name + ';'
            'Trusted_Connection=yes;'
            'Integrated Security=SSPI;'
            'Persist Security Info=True;'
            'APP=' + app_name + ';'
        )
        try:
            self.conn = pyodbc.connect(sql_connection_string)

        except pyodbc.Error as ex:
            print('[ERROR] Fatal Error: SQL Server connection can\'t be done. Server: ', server_name)
            print(ex)
            raise SystemError

    def close_connection(self):
        self.conn.close()

    def database_exists(self, dbname: str) -> bool:
        sql_stmt = """
            SELECT	    DatabaseExists = COUNT(*)
            FROM	    sys.databases
            WHERE	    [name] = ?
        """
        cursor = self.conn.cursor()
        cursor.execute(sql_stmt, dbname)
        data = cursor.fetchone()[0] == 1
        cursor.close()
        return data

    def get_table_fields(self, table: str):

        schema = table.split('.')

        if not self.database_exists(schema[0]):
            raise Exception('Selected database not found: ' + schema[0])

        sql_stmt = """
            SELECT		[COLUMN_NAME]
            FROM		[""" + schema[0] + """].INFORMATION_SCHEMA.COLUMNS
            WHERE		TABLE_CATALOG = ?
                        AND TABLE_SCHEMA = ?
                        AND TABLE_NAME = ?
            ORDER BY	ORDINAL_POSITION
        """

        cursor = self.conn.cursor()
        cursor.execute(sql_stmt, (schema[0], schema[1], schema[2]))
        data = []
        for row in cursor.fetchall():
            data.append(row[0])
        cursor.close()
        return data
