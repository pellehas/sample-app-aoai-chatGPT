import pyodbc

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=hassel.database.windows.net;"
    "DATABASE=sql;"
    "UID=hasse;"
    "PWD=Darthvader12!;"
)

cursor = conn.cursor()
cursor.execute("SELECT TOP 1 * FROM school_schedule")
row = cursor.fetchone()
print(row)

def get_schedule(student_id, day):
    query = """
    SELECT subject, start_time, end_time, room
    FROM school_schedule
    WHERE student_id = ? AND day_of_week = ?
    """
    cursor.execute(query, (student_id, day))
    rows = cursor.fetchall()

    schedule = []
    for row in rows:
        schedule.append({
            "subject": row.subject,
            "time": f"{row.start_time} - {row.end_time}",
            "room": row.room
        })

    return schedule
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key="3R4X6GB48qMPvlnMq5mXLEOY87Bu5PZnxR8iVvVNRYrpu8KKs1mbJQQJ99BLACfhMk5XJ3w3AAABACOGyIZD",
    api_version="2024-02-15-preview",
    azure_endpoint="https://hasselnot2.openai.azure.com/openai/v1/chat/completions"
)

student_id = "S001"
day = "Monday"

schedule_data = get_schedule(student_id, day)

prompt = f"""
Student ID: {student_id}
Day: {day}
Schedule Data: {schedule_data}
Question:
What classes do I have on Monday
"""

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system",
            "content": (
                "You are a school scheduling assistant. "
                "Only answer using the provided schedule data. "
                "If there are no classes, say so clearly."
            )
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print(response.choices[0].message.content)




