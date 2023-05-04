import sqlite3
import sys

connection = sqlite3.connect("/Users/andrewle/Documents/School/INFO330/INFO330-AccessingDatabases/pokemon.sqlite")
cursor = connection.cursor()

types = ["bug", "dark", "dragon", "electric", "fairy", "fight",
         "fire", "flying", "ghost", "grass", "ground", "ice", "normal",
         "poison", "psychic", "rock", "steel", "water"]

if len(sys.argv) < 6:
    print("You must give me six Pokemon to analyze!")
    sys.exit()

team = []

for i, arg in enumerate(sys.argv):
    if i == 0:
        continue
    # checks to see if input is a number or name (EXTRA CREDIT)
    if arg.isdigit():
        pokedex_number = int(arg)
        # query to select the name of the pokemon if user gives an id and saves it
        cursor.execute("SELECT name FROM pokemon WHERE id=?", (pokedex_number,))
        pokemon = cursor.fetchone()
        pokemon_name = pokemon[0]
    else:
        pokemon_name = arg
        # queries pokedex_number if given a name
        cursor.execute("SELECT id FROM pokemon WHERE name=?", (pokemon_name,))
        pokemon = cursor.fetchone()
        pokedex_number = pokemon[0]

    team.append(pokedex_number)

    # selects type id from the given pokemon and saves it.
    cursor.execute("SELECT type_id, which FROM pokemon_type WHERE pokemon_id=?", (pokedex_number,))
    type_rows = cursor.fetchall()
    type_ids = [row[0] for row in type_rows] #extracts first element in each row, in this case being type_id
    type_names = []

    # fetches types according to it's type_id
    for type_id in type_ids:
        cursor.execute("SELECT name FROM type WHERE id=?", (type_id,))
        type_names.append(cursor.fetchone()[0])
    strong_against = []
    weak_against = []

    # outer loop iterates through the pair of type_names and type_ids
    for poke_type, type_id in zip(type_names, type_ids):
        against_values = []

        # inner loop fetches the against value and appends it to against_values list with the corresponding type_name
        for against_type in types:
            column_name = f"against_{against_type}"
            cursor.execute(f"SELECT {column_name} FROM against WHERE type_source_id1=? OR type_source_id2=?", (type_id, type_id))
            against_value = cursor.fetchone()[0]
            against_values.append((against_type, against_value))

        # loop iterates through the against_values list and appends values to weak or strong against based off effectiveness
        for against_type, against_value in against_values:
            if against_value < 1:
                strong_against.append(against_type)
            elif against_value > 1:
                weak_against.append(against_type)

    strong_against = list(set(strong_against))
    weak_against = list(set(weak_against))

    # printing output from readme example
    print(f"Analyzing {pokedex_number}")
    print(f"{pokemon_name} ({' '.join(type_names)}) is strong against {strong_against} but weak against {weak_against}")

answer = input("Would you like to save this team? (Y)es or (N)o: ")
if answer.upper() == "Y" or answer.upper() == "YES":
    team_name = input("Enter the team name: ")
    connection.commit()

    print(f"Saving {team_name} ...")
else:
    print("Bye for now!")

cursor.close()
connection.close()
