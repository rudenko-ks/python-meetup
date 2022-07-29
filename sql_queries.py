import sqlite3

con = sqlite3.connect('example.db')
cur = con.cursor()


def sql_get_speaker_by_lastname(lastname: str) -> int:
    pass