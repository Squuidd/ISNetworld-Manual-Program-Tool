import sqlite3 as sq
import safety_program_creator as spc

conn = sq.connect('safety_program.db')

cur = conn.cursor()

# cur.execute("""CREATE TABLE safety_programs (
#                 name text, 
#                 path text
#                 )""")

path = spc.findPath("cranes.docx")


# cur.execute(f"INSERT INTO safety_programs VALUES (?, ?)", ("cranes", path))
cur.execute(f"INSERT INTO safety_programs VALUES (:name, :path)", {"name": "cranes", "path": path})

conn.commit()

cur.execute("SELECT * FROM safety_programs WHERE name='cranes'")

print(cur.fetchall)



conn.commit()
conn.close()