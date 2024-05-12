import sys
import ConnectToDatabase
from datetime import date

def fetch_info():
    db = ConnectToDatabase.contodb()
    if not db.is_connected():
        print("Failed to connect to the database")
        sys.exit(1)

    # select the database to work with
    cursor = db.cursor()
    cursor.execute("USE DB")


    # Get today's date
    today = date.today()

    # Convert the date to the format used in your database
    # This is just an example, you might need to adjust the format depending on your database
    today_str = today.strftime('%Y-%m-%d')

    cursor.execute(f"SELECT * FROM TASKS WHERE (STATUS = 'TODO' OR (STATUS = 'DONE' AND (DATE(CREATED_AT) = '{today_str}' OR DATE(UPDATED_AT) = '{today_str}')))") 
    rows = cursor.fetchall()

    # create a list of dictionaries, each containing one row
    tasks = []
    for row in rows:
        task = {
            'ID': row[0],
            'NAME': row[1],
            'DESCRIPTION': row[2],
            'STATUS': row[3],
            'UPLOADED_FILE_OF_COMPLETION': row[4],
            'CREATED_AT': row[5],
            'UPDATED_AT': row[6]
        }
        tasks.append(task)

    return tasks

def do_i_get_screen_time():
    # check if there are 3 tasks from today that are done
    db = ConnectToDatabase.contodb()
    if not db.is_connected():
        print("Failed to connect to the database")
        sys.exit(1)
    
    cursor = db.cursor()
    cursor.execute("USE DB")

    today = date.today()
    today_str = today.strftime('%Y-%m-%d')

    cursor.execute(f"SELECT COUNT(*) FROM TASKS WHERE REWARD = 'NOT_YET' AND STATUS = 'DONE' AND DATE(UPDATED_AT) = '{today_str}'")
    reward_not_yet_count = cursor.fetchone()[0]

    cursor.execute(f"SELECT COUNT(*) FROM TASKS WHERE REWARD = 'RECEIVED' AND STATUS = 'DONE' AND DATE(UPDATED_AT) = '{today_str}'")
    reward_count = cursor.fetchone()[0]

    print ("reward_count: ", reward_count)
    print ("reward_not_yet_count: ", reward_not_yet_count)

    if reward_not_yet_count == 3 and reward_count == 0 and reward_not_yet_count + reward_count == 3:
        cursor.execute(f"INSERT INTO SCREEN_TIME (TIME) VALUES (2700);")
        cursor.execute(f"UPDATE TASKS SET REWARD = 'RECEIVED' WHERE REWARD = 'NOT_YET' AND STATUS = 'DONE' AND DATE(UPDATED_AT) = '{today_str}'")
        db.commit()
    
    if reward_count >= 3 and reward_not_yet_count != 0:        
        while reward_count >= 3 and reward_not_yet_count != 0:
            cursor.execute(f"INSERT INTO SCREEN_TIME (TIME) VALUES (450);")
            db.commit()
            reward_not_yet_count -= 1
        cursor.execute(f"UPDATE TASKS SET REWARD = 'RECEIVED' WHERE REWARD = 'NOT_YET' AND STATUS = 'DONE' AND DATE(UPDATED_AT) = '{today_str}'")
        db.commit()

    cursor.execute("SELECT SUM(TIME) FROM SCREEN_TIME")
    screen_time = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(TIME) FROM USED_SCREEN_TIME")
    used_screen_time = cursor.fetchone()[0]

    if used_screen_time is None:
        used_screen_time = 0

    if screen_time is None:
        screen_time = 0
    
    return screen_time - used_screen_time
    