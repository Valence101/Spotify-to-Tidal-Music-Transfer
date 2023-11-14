local_state_file_path = './created_tidal_playlists.txt'

def read_created_playlists():
    try:
        with open(local_state_file_path, 'r') as file:
            created_playlists = file.readlines()
        return [name.strip() for name in created_playlists]
    except FileNotFoundError:
        return []

def write_created_playlist(playlist_name):
    with open(local_state_file_path, 'a') as file:
        file.write(f"{playlist_name}\n")
