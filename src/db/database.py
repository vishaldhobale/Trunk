import os
import sys
import sqlite3

sys.path.append(os.getcwd())
from config.constants import db_name, db_hostname, db_username, db_password
from utils.logger import SampleLogger


class SqLiteDB(SampleLogger):
    def __init__(self):
        # SampleLogger().__init__(self)
        super().__init__()

    def sql_connect(self):
        """
        :return:
        """
        try:
            conn = sqlite3.connect("dbfile/" + db_name)
            self.logger.info(f"connection to {db_name} successfully...")
            return conn
        except Exception as err:
            self.logger.error(str(err))
            return None

    def sql_disconnect(self, conn):
        """
        :param conn:
        :return:
        """
        try:
            conn.close()
            self.logger.info(f"Disconnected from database {db_name}")
        except Exception as err:
            self.logger.error(str(err))
            sys.exit(1)

    def execute_command(self, command):
        """
        :param command:
        :return:
        """
        try:
            self.logger.info(f"sql command: {command}")
            conn = self.sql_connect()
            cursor = conn.cursor()
            cursor.execute(command)
            conn.commit()
            self.logger.info(f"changes for command {command}, recoreded.")
        except Exception as err:
            self.logger.error(str(err))
        finally:
            self.sql_disconnect(conn)

    def create_table_in_db(self):
        """
        :return:
        """
        querry = """CREATE TABLE IF NOT EXISTS testcases
                    (TC_ID VARCHAR PRIMARY KEY NOT NULL,
                    TC_NAME TEXT NOT NULL,
                    SERVER_ID VARCHAR,
                    FLAG INT)"""
        self.execute_command(querry)

    def fetch_all_records_from_db(self, tablename):
        """
        :param tablename:
        :return:
        """
        querry = f"select * from {tablename}"
        con = self.sql_connect()
        cur = con.cursor()
        cur.execute(querry)
        all_data = cur.fetchall()
        self.logger.info(f"From table {tablename} all data: {all_data}")
        self.sql_disconnect(con)
        return all_data

    def insert_into_table(self, tcid, tcname, serverid, flag):
        """
        :param tcid:
        :param tcname:
        :param serverid:
        :param flag:
        :return:
        """
        try:
            if self.tcid_present_in_db("testcases", tcid):
                querry = f"UPDATE testcases SET TC_NAME='{tcname}', SERVER_ID = '{serverid}, FLAG={flag} WHERE TC_ID LIKE '{tcid}'"
                self.execute_command(querry)
                self.logger.info(f"1 row updated for id: {tcid}")
            else:
                querry = "INSERT INTO testcases (TC_ID, TC_NAME, SERVER_ID, FLAG) VALUES ('%s','%s','%s',%d)" % (tcid,
                                                                                                                 tcname,
                                                                                                                 serverid,
                                                                                                                 flag)
                self.execute_command(querry)
                self.logger.info(f"1 row inserted for id: {tcid}")
        except Exception as err:
            self.logger.error(str(err))

    def tcid_present_in_db(self, tablename, tcid):
        """
        :param tcid:
        :return:
        """
        try:
            con = self.sql_connect()
            cur = con.cursor()
            cur.execute(f"SELECT * FROM {tablename} WHERE TC_ID like '{tcid}'")
            alldata = cur.fetchall()
            self.logger.info(f"record for tcud {tcid}: {alldata}")
            self.sql_disconnect(con)
            return True if alldata else False
        except Exception as err:
            self.logger.error(str(err))
            self.sql_disconnect(con)
            return False

    def delete_entry_from_table(self, tablename, tcid):
        """
        :param id:
        :return:
        """
        try:
            if tcid is not None:
                querry = f"DELETE FROM {tablename} WHERE TC_ID LIKE '{tcid}'"
                self.execute_command(querry)
            else:
                pass
        except Exception as err:
            self.logger.error(str(err))

    def delete_all_entry_from_table(self, tablename):
        """
        :param id:
        :return:
        """
        try:
            querry = f'delete from {tablename}'
            self.execute_command(querry)
            self.logger.info(f"Removed all recoreds from table {tablename}")
        except Exception as err:
            self.logger.error(str(err))


if __name__ == "__main__":
    d = SqLiteDB()
    # con = d.sql_connect()
    # d.sql_disconnect(con)
    # d.create_table_in_db()
    # for i in range(20):
    #     d.insert_into_table("tc%s" % str(i), "test case %s" % str(i), "server%s" % str(i), int(i))
    # print(d.fetch_all_records_from_db('testcases'))
    # print(d.tcid_present_in_db('testcases', 'tc0'))
    # print(d.delete_all_entry_from_table('testcases'))
    # print("After record removed.")
    # print(d.fetch_all_records_from_db('testcases'))
