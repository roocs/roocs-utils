import os

try:
    from abcunit_backend.base_handler import BaseHandler
except ImportError:
    raise

try:
    import psycopg2
    from psycopg2.extras import Json
except ImportError:
    raise

from roocs_utils.project_utils import derive_ds_id


class DataBaseHandler(BaseHandler):
    def __init__(self, table_name="results"):
        """
        :param table_name: (str) Optional string name of the table logs will be insert into (default is 'results')
        """

        self.connection_info = os.environ.get("ABCUNIT_DB_SETTINGS")
        if not self.connection_info:
            raise KeyError(
                "Please create environment variable ABCUNIT_DB_SETTINGS"
                'in for format of "dbname=<db_name> user=<user_name>'
                'host=<host_name> password=<password>"'
            )

        self._test_connection()
        self.table_name = table_name
        self._create_table()

    def _test_connection(self):
        try:
            conn = psycopg2.connect(self.connection_info)
        except psycopg2.Error as err:
            print(err)
            raise ValueError(
                "ABCUNIT_DB_SETTINGS string is incorrect. Should be"
                'in for format of "dbname=<db_name> user=<user_name>'
                'host=<host_name> password=<password>"'
            )

        conn.close()

    def _create_table(self):
        """
        Creates a table called <self.table_name> with primary key id varchar(255), result varchar(255),
        content json, error text if one does not already exist.
        """

        with psycopg2.connect(self.connection_info) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"CREATE TABLE IF NOT EXISTS {self.table_name}"
                    "(id varchar(255) PRIMARY KEY, result varchar(255) NOT NULL, content json, error text);"
                )
                conn.commit()

    def _delete_table(self):
        """
        Drops the database table
        """

        with psycopg2.connect(self.connection_info) as conn:
            with conn.cursor() as cur:
                cur.execute(f"DROP TABLE {self.table_name};")
                conn.commit()

    def get_result_status(self, identifier):
        """
        Selects the result of the job of the identifier and returns it
        :param identifier: (str) Identifier of the job result
        :return: (str) Result of job
        """

        query = f"SELECT result FROM {self.table_name} " f"WHERE id='{identifier}';"

        with psycopg2.connect(self.connection_info) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                if cur.rowcount > 0:
                    return cur.fetchone()[0]

        return None

    def get_content(self, identifier):
        """
        Selects the content of the job of the identifier and returns it
        :param identifier: (str) Identifier of the job result
        :return: (dict) Content scanned for identifier
        """

        query = f"SELECT content FROM {self.table_name} " f"WHERE id='{identifier}';"

        with psycopg2.connect(self.connection_info) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                if cur.rowcount > 0:
                    return cur.fetchone()[0]

        return None

    def get_all_content(self):
        """
        Selects the content of all the successful jobs
        :return: (list) List of dicts containg scanned content
        """

        query = f"SELECT content FROM {self.table_name} " f"WHERE result='success';"

        with psycopg2.connect(self.connection_info) as conn:
            with conn.cursor() as cur:
                cur.execute(query)

                return [name[0] for name in cur]

    def get_error_traceback(self, identifier):
        """
        Selects the error traceback of the job of the identifier and returns it
        :param identifier: (str) Identifier of the job result
        :return: (str) Error traceback for identifier
        """

        query = f"SELECT error FROM {self.table_name} " f"WHERE id='{identifier}';"

        with psycopg2.connect(self.connection_info) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                if cur.rowcount > 0:
                    return cur.fetchone()[0]

        return None

    def get_successful_runs(self):
        """
        :return: (str list) Returns a list of the identifiers of all successful runs
        """

        query = f"SELECT id FROM {self.table_name} " "WHERE result='success';"

        with psycopg2.connect(self.connection_info) as conn:
            with conn.cursor() as cur:
                cur.execute(query)

                return [name[0] for name in cur]

    def get_failed_runs(self):
        """
        :return: (dict) Dictionary of error types mapped to lists of job identifiers which result in them
        """

        query = f"SELECT id, result FROM {self.table_name} " "WHERE result<>'success';"

        with psycopg2.connect(self.connection_info) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                failures = {}
                for (name, result) in cur:
                    failures.setdefault(result, [])
                    failures[result].append(name)

        return failures

    def delete_result(self, identifier):
        """
        Deletes entry specified by the given identifierfrom the database
        :param identifier: (str) Identifier of the job
        """

        query = f"DELETE FROM {self.table_name} " f"WHERE id='{identifier}';"

        with psycopg2.connect(self.connection_info) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                conn.commit()

    def delete_all_results(self):
        """
        Deletes all entries from the table
        """

        with psycopg2.connect(self.connection_info) as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {self.table_name};")
                conn.commit()

    def ran_successfully(self, identifier):
        """
        Returns true / false on whether the result with this identifier is successful
        :param identifier: (str) Identifier of the job result
        :return: (bool) Boolean on if job ran successfully
        """

        query = f"SELECT result FROM {self.table_name} " f"WHERE id='{identifier}';"

        with psycopg2.connect(self.connection_info) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchone()
                if result is not None:
                    return result[0] == "success"

        return False

    def count_results(self):
        """
        :return: (int) Number of results in the table
        """

        with psycopg2.connect(self.connection_info) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT COUNT(*) FROM {self.table_name};")

                return cur.fetchone()[0]

    def count_successes(self):
        """
        :return: (int) Number of successful results in the table
        """

        query = f"SELECT COUNT(*) FROM {self.table_name} " "WHERE result='success';"

        with psycopg2.connect(self.connection_info) as conn:
            with conn.cursor() as cur:
                cur.execute(query)

                return cur.fetchone()[0]

    def count_failures(self):
        """
        :return: (int) Number of failed results in the table
        """

        query = f"SELECT COUNT(*) FROM {self.table_name} " "WHERE result<>'success';"

        with psycopg2.connect(self.connection_info) as conn:
            with conn.cursor() as cur:
                cur.execute(query)

                return cur.fetchone()[0]

    def insert_success(self, identifier, content):
        """
        Inserts an entry into the table with a given identifier, the result 'success' and the content of the scan for this identifier
        :param identifier: (str) Identifier of the job
        :parma content: (dict) The scanned content for the intake catalog
        """
        query = (
            f"INSERT INTO {self.table_name}(id, result, content) "
            f"VALUES (%s, %s, %s);"
        )

        with psycopg2.connect(self.connection_info) as conn:
            with conn.cursor() as cur:
                cur.execute(query, [f"{identifier}", "success", Json(content)])
                conn.commit()

    def insert_failure(self, identifier, error_type, traceback):
        """
        Inserts an entry into the table with a given identifier and erroneous result
        :param identifier: (str) Identifier of the job
        :param error_type: (str) Result of the job
        :param traceback: (str) The traceback from the error
        """

        query = (
            f"INSERT INTO {self.table_name}(id, result, error) " f"VALUES (%s, %s, %s);"
        )

        with psycopg2.connect(self.connection_info) as conn:
            with conn.cursor() as cur:
                cur.execute(query, [f"{identifier}", f"{error_type}", f"{traceback}"])
                conn.commit()

    def get_successful_datasets(self):
        """
        :return: (set) Dataset ids recorded in the table
        """

        query = f"SELECT id FROM {self.table_name} " "WHERE result='success';"

        with psycopg2.connect(self.connection_info) as conn:
            with conn.cursor() as cur:
                cur.execute(query)

                return {derive_ds_id(name[0]) for name in cur}

    def get_failed_datasets(self):
        """
        :return: (set) Dataset ids which have recorded failures
        """

        query = f"SELECT id FROM {self.table_name} " "WHERE result<>'success';"

        with psycopg2.connect(self.connection_info) as conn:
            with conn.cursor() as cur:
                cur.execute(query)

                return {derive_ds_id(name[0]) for name in cur}

    def get_all_datasets(self):
        """
        :return: (set) All Dataset ids recorded in the table
        """

        query = f"SELECT id FROM {self.table_name} "

        with psycopg2.connect(self.connection_info) as conn:
            with conn.cursor() as cur:
                cur.execute(query)

                return {derive_ds_id(name[0]) for name in cur}
