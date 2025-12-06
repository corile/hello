import sqlite3
from pathlib import Path
import sys


def setup_db_connection():
    conn = sqlite3.connect("C:\\Users\\piyus\\hello\\db.sqlite3", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cursor = conn.cursor()
    return conn, cursor

def load_required_entities(cur):
    # Fetch all travel agency IDs from the database
    cur.execute("SELECT id, name FROM hotelrebates_travelagency")
    all_travel_agencies = {name: id for id, name in cur.fetchall()}
    print(f'Found {len(all_travel_agencies)} travel agencies.')

    # Fetch all portals from the database
    cur.execute("SELECT id, name FROM hotelrebates_cashbackportal")
    all_portals = {name: id for id, name in cur.fetchall()}
    print(f'Found {len(all_portals)} portals.')

    if (len(all_travel_agencies) < 1 or len(all_portals) < 1):
        print('Failed to retrieve data from DB. Exiting...')
        sys(exit)
    return all_travel_agencies, all_portals
    
conn, cursor = setup_db_connection()
all_travel_agencies, all_portals = load_required_entities(cursor)

def get_last_seen_time(portal, travel_agency):
    cursor.execute(
        'SELECT MAX(last_seen) as "[timestamp]" FROM hotelrebates_portaloffer where portal_id = ? and travel_agency_id = ?', 
        (all_portals[portal], all_travel_agencies[travel_agency]))
    last_seen_time = cursor.fetchone()
    return last_seen_time[0]

def save_row_portal_cashback_without_commit(portal, travel_agency, cashback_rate, terms_and_conditions):
    cursor.execute("""
            INSERT INTO hotelrebates_portaloffer (portal_id, travel_agency_id, cashback_rate, terms_and_conditions, last_seen)
            VALUES (?, ?, ?, ?, datetime('now'))
        """, (all_portals[portal], all_travel_agencies[travel_agency], cashback_rate, terms_and_conditions))
    
def commit_all_and_close():
    conn.commit()
    conn.close()