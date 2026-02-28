from auth import get_spotify_client

def main():
    sp = get_spotify_client()
    user = sp.current_user()
    print(f"Conectado como: {user['display_name']}")

if __name__ == "__main__":
    main()