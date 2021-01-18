required_tables = ["Author", "Novel", "Entity", "BodyCategory", "BodyPart", "Ownership"]

def process(tallies, database):
    
    #does the database have the right tables in it?
    for i in required_tables:
        if not table_exists(i, database):
            return "Error: missing tables"
        


    #for each entity

    #for each word

def table_exists(name,database):
    print(name)
    cursor = database.cursor()
    cursor.execute(
            "SELECT * FROM sqlite_master WHERE type='table' AND name=(?);", (name,))
    answer = cursor.fetchone()
    if answer == None:
        return False
    else:
        return True
