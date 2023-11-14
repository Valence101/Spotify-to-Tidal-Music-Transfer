import json
import SpotifyHandler
import TidalHandler
import StateHandler

title = r"""
  _________              __  .__  _____          __           ___________.__    .___      .__    ___________                              _____             
 /   _____/_____   _____/  |_|__|/ ____\__.__. _/  |_  ____   \__    ___/|__| __| _/____  |  |   \__    ___/___________    ____   _______/ ____\___________ 
 \_____  \\____ \ /  _ \   __\  \   __<   |  | \   __\/  _ \    |    |   |  |/ __ |\__  \ |  |     |    |  \_  __ \__  \  /    \ /  ___/\   __\/ __ \_  __ \
 /        \  |_> >  <_> )  | |  ||  |  \___  |  |  | (  <_> )   |    |   |  / /_/ | / __ \|  |__   |    |   |  | \// __ \|   |  \\___ \  |  | \  ___/|  | \/
/_______  /   __/ \____/|__| |__||__|  / ____|  |__|  \____/    |____|   |__\____ |(____  /____/   |____|   |__|  (____  /___|  /____  > |__|  \___  >__|   
        \/|__|                         \/                                        \/     \/                             \/     \/     \/            \/     
                                                                                                                                by Almethis  
"""


client_id = input("Please enter your Spotify Client ID (You get this from the devloper dashboard: ")
client_secret = input("Please enter your Client Secret: ")
user_id = input("Please enter your Spotify user id: You can get this from visting your profile. The URL will look like https://open.spotify.com/user/<Your user ID you need to paste here>")



#Spotify Login
spotify_login = SpotifyHandler.login(client_id, client_secret)
spotify_playlists = SpotifyHandler.request_all_playlist(spotify_login, user_id)

print("Located the following playlist: ", spotify_playlists.keys())
#Tidal login
tidal_login = TidalHandler.login()


for playlist_name in spotify_playlists.keys():
    # Check if we've already created this playlist in TIDAL
    created_playlists = StateHandler.read_created_playlists()

    if playlist_name not in created_playlists:
        print(f"Playlist: '{playlist_name}' does not exist within TIDAL, creating now...")
        spotify_playlist = SpotifyHandler.request_tracks(spotify_login, spotify_playlists[playlist_name])

        # How we will keep track of how many songs we need to port over / used to move offset forward. 
        total_songs = spotify_playlist["total"]
        # Creating an empty Play List
        tidal_playlist = TidalHandler.create_playlist(tidal_login,playlist_name)

        offset = 0

        while total_songs > 0:
            TidalHandler.build_playlist(tidal_login, tidal_playlist, spotify_playlist)
            offset = offset +100
            total_songs= total_songs - 100
            spotify_playlist = SpotifyHandler.request_tracks(spotify_login, spotify_playlists[playlist_name], offset)
            if offset > total_songs:
                break
        
        # Update the state file to record the fact that we have created this playlist within TIDAL
        StateHandler.write_created_playlist(playlist_name)
    else:
        print(f"Playlist: '{playlist_name}' already exists. Skipping creation.")

