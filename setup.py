from modules.load_config import get_database

def set_defaults():
    database = get_database()
    database.set_media_server_configuration(
        SubscriberPlaylistTitleTemplate =  "{}'s Playlist",
        SubscriberWatchlistTitleTemplate =  "{}'s Watchlist"
    )  # will only set if first entry doesn't exist