from pydantic import BaseModel

DB_MODEL_TO_SQLITE_COLS = {
    'film_work': (
        'id', 'title', 'description',
        'creation_date', 'rating',
        'type', 'created_at', 'updated_at'
    ),
    'genre': (
        'id', 'name', 'description', 'created_at', 'updated_at'
    ),
    'person': (
        'id', 'full_name', 'created_at', 'updated_at'
    ),
    'genre_film_work': (
        'id', 'film_work_id', 'genre_id', 'created_at'
    ),
    'person_film_work': (
        'id', 'film_work_id', 'person_id', 'created_at', 'role'
    )
}


class PGController:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.cursor.execute('SET LOCAL search_path TO content')

    def load_to_db(self, table: BaseModel, data: list[BaseModel]):
        cols = table.model_fields.keys()
        table_name = table.model_json_schema()['title']
        sql_stmt = (
            f'INSERT INTO {table_name} ({",".join(cols)}) '
            f'VALUES ({("%s," * len(cols)).rstrip(",")})'
        )
        for x in data:
            self.cursor.execute(sql_stmt, tuple(x.model_dump().values()))


class SqliteController:
    def __init__(self, connection):
        self.connection = connection

    def extract_data(self, table: BaseModel, n):
        curs = self.connection.cursor()
        table_name = table.model_json_schema()['title']
        cols = ','.join(DB_MODEL_TO_SQLITE_COLS[table_name])
        curs.execute(f'select {cols} from {table_name}')
        while True:
            data = [
                table.model_validate(dict(x)) for x in curs.fetchmany(n)]
            if not data:
                return
            yield data
