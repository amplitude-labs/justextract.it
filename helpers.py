from typing import Optional
import uuid
import psycopg2
import os


class Connection:
    def __init__(self, rds):
        self.rds = rds
        self.conn = None

    def __enter__(self):
        self.conn = psycopg2.connect(user=os.environ['RDS_USER'], password=os.environ['RDS_PASSWORD'],
                                     host=os.environ['RDS_HOST'], port=os.environ['RDS_PORT'], database=os.environ['RDS_DATABASE'])
        return self.conn

    def __exit__(self, *args):
        self.conn.close()


def update_status(id: str, percentage: int, status: str, nodes: Optional[dict]):
    with Connection("rds") as db:
        with db.cursor() as cursor:
            cursor.execute(
                "UDPATE jei_tasks SET percentage=%s, status=%s, nodes=%s WHERE id=%s", (percentage, status, nodes, id))
            db.commit()


def create_task(key_id: str):
    with Connection("rds") as db:
        with db.cursor() as cursor:
            cursor.execute(
                "INSERT INTO jei_tasks VALUES (%s, NULL, NULL, NULL, %s)", (uid := str(uuid.uuid4()), key_id))
            db.commit()
            return uid
