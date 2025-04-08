import pandas as pd
import sqlite3

# Wczytaj pliki CSV do DataFrame'ów
stations_df = pd.read_csv('clean_stations.csv')
measure_df = pd.read_csv('clean_measure.csv')

# Połącz się z bazą danych SQLite
conn = sqlite3.connect('database.db')

# Zapisz DataFrame'y do tabel SQL
stations_df.to_sql(name='stations', con=conn, index=False, if_exists='replace')
measure_df.to_sql(name='measure', con=conn, index=False, if_exists='replace')

# Wykonaj zapytanie
result = conn.execute("SELECT * FROM stations LIMIT 5").fetchall()

# Wyświetl wynik zapytania
for row in result:
    print(row)

# Zamknij połączenie
conn.close()