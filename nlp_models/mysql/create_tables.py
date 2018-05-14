"""
This module creates the tables in the mysql that will store the
data from web service.
"""


from Daka.robot.database.mysql import Mysql
from Daka.robot.utils.conf import UtilConf
from Daka.robot.const.common import TPL_MYSQL_KEY


def create_tables(db, cur):

    cur.execute("""
                CREATE TABLE robot_text_template
                (
                id INT NOT NULL AUTO_INCREMENT,
                raw_text TEXT NOT NULL,
                std_text TEXT NOT NULL,
                template_id INT,
                scene_id INT NOT NULL,
                start_time TEXT NOT NULL,
                PRIMARY KEY (id)
                )
                """)
    db.commit()
    cur.close()
    db.close()


if __name__ == "__main__":
    params_tpl_mysql = UtilConf()[TPL_MYSQL_KEY]
    mysql = Mysql(**params_tpl_mysql)
    create_tables(mysql.conn, mysql.cursor)
