import mysql.connector
import tempfile
from PyPDF2 import PdfReader
import webbrowser


def alterResume(name):
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="resumes"
    )

    cursor = conn.cursor()
    sql = "SELECT file_data FROM resume WHERE full_name = %s"
    record_id = name

    cursor.execute(sql, (record_id,))

    result = cursor.fetchone()

    file_data = result[0]
    cursor.close()
    conn.close()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(file_data)

    webbrowser.open("file://" + temp_file.name)
    temp_file.close()




