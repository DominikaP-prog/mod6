import sqlite3
from sqlite3 import Error

create_projects_sql = """
-- projects table
CREATE TABLE IF NOT EXISTS projects (
  id integer PRIMARY KEY,
  nazwa text NOT NULL,
  start_date text,
  end_date text
);
"""

create_tasks_sql = """
-- zadanie table
CREATE TABLE IF NOT EXISTS tasks (
  id integer PRIMARY KEY,
  project_id integer NOT NULL,
  nazwa VARCHAR(250) NOT NULL,
  opis TEXT,
  status VARCHAR(15) NOT NULL,
  start_date text NOT NULL,
  end_date text NOT NULL,
  FOREIGN KEY (project_id) REFERENCES projects (id)
);
"""

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        with sqlite3.connect(db_file) as conn:
            print(f"Connected to {db_file}, sqlite version: {sqlite3.version}")
            return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

def create_tables(conn, create_projects_sql, create_tasks_sql):
    """ create tables in the SQLite database"""
    try:
        cursor = conn.cursor()
        cursor.execute(create_projects_sql)
        cursor.execute(create_tasks_sql)
        print("Tables created successfully.")
    except Error as e:
        print(e)

def add_project(conn, project):
    """
    Create a new project into the projects table
    :param conn: Connection object
    :param project: tuple (nazwa, start_date, end_date)
    :return: project id
    """
    sql = '''INSERT INTO projects(nazwa, start_date, end_date)
             VALUES(?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid

def add_task(conn, task):
    """
    Create a new task into the tasks table
    :param conn: Connection object
    :param task: tuple (project_id, nazwa, opis, status, start_date, end_date)
    :return: task id
    """
    sql = '''INSERT INTO tasks(project_id, nazwa, opis, status, start_date, end_date)
             VALUES(?,?,?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()
    return cur.lastrowid

def update_project(conn, project):
    """
    Update a project in the projects table
    :param conn: Connection object
    :param project: tuple (nazwa, start_date, end_date, id)
    :return: None
    """
    sql = '''UPDATE projects
             SET nazwa = ?,
                 start_date = ?,
                 end_date = ?
             WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()

def update_task(conn, task):
    """
    Update a task in the tasks table
    :param conn: Connection object
    :param task: tuple (project_id, nazwa, opis, status, start_date, end_date, id)
    :return: None
    """
    sql = '''UPDATE tasks
             SET project_id = ?,
                 nazwa = ?,
                 opis = ?,
                 status = ?,
                 start_date = ?,
                 end_date = ?
             WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()

def delete_project(conn, id):
    """
    Delete a project by project id
    :param conn: Connection object
    :param id: id of the project
    :return: None
    """
    sql = 'DELETE FROM projects WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()

def delete_task(conn, id):
    """
    Delete a task by task id
    :param conn: Connection object
    :param id: id of the task
    :return: None
    """
    sql = 'DELETE FROM tasks WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()

def fetch_projects(conn):
    """
    Query all rows in the projects table
    :param conn: the Connection object
    :return: a list of projects
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM projects")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    return rows

def fetch_tasks(conn, project_id):
    """
    Query tasks by project_id
    :param conn: the Connection object
    :param project_id: id of the project
    :return: a list of tasks
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE project_id=?", (project_id,))
    rows = cur.fetchall()
    for row in rows:
        print(row)
    return rows

if __name__ == '__main__':
    conn = create_connection("database.db")
    
    if conn is not None:
        # Dodanie przykładowego projektu
        project = ("Powtórka z angielskiego", "2020-05-11 00:00:00", "2020-05-13 00:00:00")
        pr_id = add_project(conn, project)
        
        # Dodanie przykładowego zadania
        task = (pr_id, "Nauka słówek", "Powtórka słówek z rozdziału 1", "w trakcie", "2020-05-11 00:00:00", "2020-05-11 01:00:00")
        task_id = add_task(conn, task)
        
        print(f"Added project with id: {pr_id}")
        print(f"Added task with id: {task_id}")
        
        # Aktualizacja projektu
        updated_project = ("Powtórka z angielskiego - zaktualizowana", "2020-05-12 00:00:00", "2020-05-14 00:00:00", pr_id)
        update_project(conn, updated_project)
        
        # Aktualizacja zadania
        updated_task = (pr_id, "Nauka słówek - zaktualizowana", "Powtórka słówek z rozdziału 1 - zaktualizowana", "ukończone", "2020-05-12 00:00:00", "2020-05-12 01:00:00", task_id)
        update_task(conn, updated_task)
        
        # Usunięcie zadania
        delete_task(conn, task_id)
        
        # Usunięcie projektu
        delete_project(conn, pr_id)
        
        print("Project and task updated and deleted successfully.")
        
        # Pobieranie danych
        print("\nProjects:")
        fetch_projects(conn)
        
        print("\nTasks for project with id 1:")
        fetch_tasks(conn, 1)