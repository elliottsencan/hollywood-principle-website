import sys
import spotipy

hpAlbums = []
yamlOutput = '''- name: "{0}"
  spotify_url: "{1}"
  image_url_small : "{2}"
  image_url_medium : "{3}"
  spotify_uri : "{4}"
  '''

filename = "./_data/albums.yml"

class HPAlbum:
    def __init__(self, album):
        self.name = album["name"]
        self.spotify_url = album["external_urls"]["spotify"]
        self.image_url_small = album["images"][0]["url"]
        self.image_url_medium = album["images"][1]["url"]
        self.spotify_uri = album["uri"]
    def toYaml(self):
        return yamlOutput.format(self.name, self.spotify_url, self.image_url_small, self.image_url_medium, self.spotify_uri)


def overwrite_data_file():
    print "We're going to overwrite %r with new data." % filename
    print "If you don't want that, hit CTRL-C (^C)."
    print "If you do want that, hit RETURN."

    raw_input("?")

    print "Opening the file..."
    target = open(filename, 'w')

    print "Truncating the file.  Goodbye!"
    target.truncate()

    print "Now adding new data..."
    for hpAlbum in hpAlbums:
        target.write(hpAlbum.toYaml())
        target.write("\n")


def get_artist(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None

def show_artist_albums(artist):
    albums = []
    results = sp.artist_albums(artist['id'])
    albums.extend(results['items'])
    for album in albums:
        hpAlbums.append(HPAlbum(album))

    for hpAlbum in hpAlbums:
        print(hpAlbum.name)
        print(hpAlbum.image_url_small)

if __name__ == '__main__':
    sp = spotipy.Spotify()

    if len(sys.argv) < 2:
        print(('Usage: {0} artist name'.format(sys.argv[0])))
    else:
        name = ' '.join(sys.argv[1:])
        artist = get_artist(name)
        if artist:
            show_artist_albums(artist)
            overwrite_data_file()
        else:
            print("Can't find that artist")
