import qbittorrentapi as qbt


def connect_to_qbt(host, port, username, password):
    """Connect to qBittorrent client using the provided credentials.

    :param host: Hostname or IP address of the qBittorrent client.
    :param port: Port number of the qBittorrent client.
    :param username: Username for authentication.
    :param password: Password for authentication.
    :return: An authenticated qBittorrent API client instance.
    """
    client = qbt.Client(host=host, port=port, username=username, password=password)
    client.auth_log_in()
    return client


def get_our_torrents(client):
    """Retrieve torrents from the qBittorrent client.

    :param client: An authenticated qBittorrent API client instance.
    :return: A list of torrents.
    """
    return client.torrents_info(category="fastlibrarian", status_filter="all")


def add_torrent(client, magnet_link, save_path):
    """Add a torrent to the qBittorrent client.

    :param client: An authenticated qBittorrent API client instance.
    :param torrent_file: Path to the torrent file to be added.
    :param save_path: Directory where the torrent should be saved.
    :return: The result of the add torrent operation.
    """
    return client.torrents_add(magnet=magnet_link, category="fastlibrarian")
