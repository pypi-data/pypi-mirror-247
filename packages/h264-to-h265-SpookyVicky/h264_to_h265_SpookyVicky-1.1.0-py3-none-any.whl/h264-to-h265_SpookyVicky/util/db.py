import json

tasklist = []

def db_load():
    try:
        with open("db.json", 'r') as db:
            tasklist = json.load(db)
            return tasklist
    except:
        return False
            
def db_save(tasklist = []):
    with open("db.json", 'w') as db:
        json.dump(tasklist, db, indent=4)