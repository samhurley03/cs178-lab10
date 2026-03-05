# marquette_interface.py
# CRUD interface for the DynamoDB Marquette table

import boto3

REGION = "us-east-1"
TABLE_NAME = "Marquette"


def get_table():
    dynamodb = boto3.resource("dynamodb", region_name=REGION)
    return dynamodb.Table(TABLE_NAME)


def print_player(player):
    name = player.get("Player Name", "Unknown")
    number = player.get("Number", "Unknown")
    position = player.get("Position", "Unknown")

    print(f"  Name     : {name}")
    print(f"  Number   : {number}")
    print(f"  Position : {position}")
    print()


# CREATE
def create_player():
    table = get_table()

    name = input("Enter player name: ")
    number = input("Enter jersey number: ")
    position = input("Enter position: ")

    table.put_item(
        Item={
            "Player Name": name,
            "Number": number,
            "Position": position
        }
    )

    print("Player added.")


# READ
def print_all_players():
    table = get_table()

    response = table.scan()
    items = response.get("Items", [])

    if not items:
        print("No players found.")
        return

    print(f"\nFound {len(items)} player(s):\n")

    for player in items:
        print_player(player)


# UPDATE
def update_player():
    table = get_table()

    name = input("Enter player name to update: ")
    number = input("Enter new jersey number: ")
    position = input("Enter new position: ")

    table.update_item(
        Key={"Player Name": name},
        UpdateExpression="SET #n = :num, #p = :pos",
        ExpressionAttributeNames={
            "#n": "Number",
            "#p": "Position"
        },
        ExpressionAttributeValues={
            ":num": number,
            ":pos": position
        }
    )

    print("Player updated.")


# DELETE
def delete_player():
    table = get_table()

    name = input("Enter player name to delete: ")

    table.delete_item(
        Key={"Player Name": name}
    )

    print("Player deleted (if existed).")


# QUERY (lookup one player)
def query_player():
    table = get_table()

    name = input("Enter player name to search: ")

    response = table.get_item(Key={"Player Name": name})

    if "Item" not in response:
        print("Player not found.")
        return

    print("\nPlayer found:\n")
    print_player(response["Item"])


def print_menu():
    print("----------------------------")
    print("Press C: CREATE a player")
    print("Press R: READ all players")
    print("Press U: UPDATE a player")
    print("Press D: DELETE a player")
    print("Press Q: QUERY a player")
    print("Press X: EXIT")
    print("----------------------------")


def main():
    input_char = ""

    while input_char.upper() != "X":
        print_menu()
        input_char = input("Choice: ")

        if input_char.upper() == "C":
            create_player()
        elif input_char.upper() == "R":
            print_all_players()
        elif input_char.upper() == "U":
            update_player()
        elif input_char.upper() == "D":
            delete_player()
        elif input_char.upper() == "Q":
            query_player()
        elif input_char.upper() == "X":
            print("exiting...")
        else:
            print("Not a valid option. Try again.")


if __name__ == "__main__":
    main()