import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIPY_CLIENT_ID = '<your id>'
SPOTIPY_CLIENT_SECRET = '<your secret>'
SPOTIPY_REDIRECT_URI = 'http://example.com'
SCOPE = "playlist-modify-private"
CACHE_PATH = "token.txt"

continue_asking = True
while continue_asking:
    year = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
    try:
        get_date = int(year.split("-")[2])
        get_month = int(year.split("-")[1])
        get_year = year.split("-")[0]
    except IndexError:
        print("Please type in a proper date format")
    else:
        if get_date <= 31 and get_month <= 12:
            if len(year.split("-")[0]) == 4 and len(year.split("-")[1]) == 2 and len(year.split("-")[2]) == 2:
                r = requests.get(url=f"https://www.billboard.com/charts/hot-100/{year}/")
                song_data = r.text
                soup = BeautifulSoup(song_data, "html.parser")
                billboard = soup.select("li .o-chart-results-list__item h3")
                song_list = [i.get_text().strip() for i in billboard]
                ## --------------------Authenticate using spotipy and generates a token access--------------##
                ## we need to pass the arguments as keyword arguments or else it will not work properly ##
                sp = spotipy.Spotify(
                    auth_manager=SpotifyOAuth(
                        client_id=SPOTIPY_CLIENT_ID,
                        client_secret=SPOTIPY_CLIENT_SECRET,
                        redirect_uri=SPOTIPY_REDIRECT_URI,
                        scope=SCOPE,
                        cache_path=CACHE_PATH
                    )
                )
                ## Get the current user ID ##
                user_id = sp.current_user()["id"]
                ## Search for the songs links from the scrapped songs list ##
                song_uri = []
                for song in song_list:
                    result = sp.search(q=f"track:{song} year:{get_year}", type="track")
                    try:
                        get_uri = result["tracks"]['items'][0]['uri']
                        song_uri.append(get_uri)
                    except IndexError:
                        print(f"No songs found for song {song}")
                ## creating and adding to spotify playlist ##
                playlist = sp.user_playlist_create(user=user_id, name=f"{year} Billboard 100", public=False)
                # print(playlist)
                ## Adding songs to playlist ##
                sp.playlist_add_items(playlist_id=playlist['id'], items=song_uri)

                continue_asking = False
            else:
                print("Please include a zero infront of the date. If your specified date or month is a "
                      "single digit number")
        else:
            print("Check your date or month and enter a correct value")
