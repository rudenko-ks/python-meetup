import sqlite3


def sql_get_conference() -> list:
    with sqlite3.connect("db.sqlite3") as con:
        cur = con.cursor()
        sql_query = """SELECT name_conf FROM Conference_conference"""
        cur.execute(sql_query)
        records = cur.fetchall()
    return records


def sql_get_performances_time(conference: str) -> list:
    with sqlite3.connect("db.sqlite3") as con:
        cur = con.cursor()
        sql_query = """
            SELECT Conference_performance.time_performance
            FROM Conference_performance
            WHERE Conference_performance.conference_id 
            IN (SELECT Conference_conference.id FROM Conference_conference WHERE Conference_conference.name_conf = ?);
        """
        cur.execute(sql_query, (conference,))
        records = cur.fetchall()
    return records


def sql_get_conference_performance() -> list:
    with sqlite3.connect("db.sqlite3") as con:
        cur = con.cursor()
        sql_query = """SELECT performance_name FROM Conference_performance"""
        cur.execute(sql_query)
        records = cur.fetchall()
    return records
    

def sql_get_speaker_by_lastname(full_name: str) -> int:
    fullname = full_name.split()
    with sqlite3.connect("db.sqlite3") as con:
        cur = con.cursor()
        sql_query = """SELECT tg_speaker_id FROM Conference_speaker WHERE last_name=? AND first_name=?"""
        cur.execute(sql_query, fullname)
        record = cur.fetchone()

    return int(record[0])
    