from replit import db

def clear_all_entries():
    keys_to_delete = [key for key in db.keys()]
    for key in keys_to_delete:
        del db[key]
        print(f"Deleted key: {key}")

if __name__ == "__main__":
    clear_all_entries()
    print("All entries cleared.")