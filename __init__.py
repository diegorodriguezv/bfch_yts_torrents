import chanutils.torrent
from chanutils import get_json, movie_title_year
from playitem import TorrentPlayItem, PlayItemList

_SEARCH_URL = 'https://yts.to/api/v2/list_movies.json'

_FEEDLIST = [
  {'title':'Latest', 'url':'https://yts.to/api/v2/list_movies.json?limit=50'},
  {'title':'Highest Rated', 'url':'https://yts.to/api/v2/list_movies.json?sort_by=rating&limit=50'},
  {'title':'Action', 'url':'https://yts.to/api/v2/list_movies.json?genre=action&sort_by=rating&limit=50'},
  {'title':'Adventure', 'url':'https://yts.to/api/v2/list_movies.json?genre=adventure&sort_by=rating&limit=50'},
  {'title':'Animation', 'url':'https://yts.to/api/v2/list_movies.json?genre=animation&sort_by=rating&limit=50'},
  {'title':'Biography', 'url':'https://yts.to/api/v2/list_movies.json?genre=biography&sort_by=rating&limit=50'},
  {'title':'Comedy', 'url':'https://yts.to/api/v2/list_movies.json?genre=comedy&sort_by=rating&limit=50'},
  {'title':'Crime', 'url':'https://yts.to/api/v2/list_movies.json?genre=crime&sort_by=rating&limit=50'},
  {'title':'Documentary', 'url':'https://yts.to/api/v2/list_movies.json?genre=documentary&sort_by=rating&limit=50'},
  {'title':'Drama', 'url':'https://yts.to/api/v2/list_movies.json?genre=drama&sort_by=rating&limit=50'},
  {'title':'Family', 'url':'https://yts.to/api/v2/list_movies.json?genre=family&sort_by=rating&limit=50'},
  {'title':'Fantasy', 'url':'https://yts.to/api/v2/list_movies.json?genre=fantasy&sort_by=rating&limit=50'},
  {'title':'Film-Noir', 'url':'https://yts.to/api/v2/list_movies.json?genre=filmnoir&sort_by=rating&limit=50'},
  {'title':'History', 'url':'https://yts.to/api/v2/list_movies.json?genre=history&sort_by=rating&limit=50'},
  {'title':'Horror', 'url':'https://yts.to/api/v2/list_movies.json?genre=horror&sort_by=rating&limit=50'},
  {'title':'Music', 'url':'https://yts.to/api/v2/list_movies.json?genre=music&sort_by=rating&limit=50'},
  {'title':'Musical', 'url':'https://yts.to/api/v2/list_movies.json?genre=musical&sort_by=rating&limit=50'},
  {'title':'Mystery', 'url':'https://yts.to/api/v2/list_movies.json?genre=mystery&sort_by=rating&limit=50'},
  {'title':'Romance', 'url':'https://yts.to/api/v2/list_movies.json?genre=romance&sort_by=rating&limit=50'},
  {'title':'Sci-Fi', 'url':'https://yts.to/api/v2/list_movies.json?genre=scifi&sort_by=rating&limit=50'},
  {'title':'Sport', 'url':'https://yts.to/api/v2/list_movies.json?genre=sport&sort_by=rating&limit=50'},
  {'title':'Thriller', 'url':'https://yts.to/api/v2/list_movies.json?genre=thriller&sort_by=rating&limit=50'},
  {'title':'War', 'url':'https://yts.to/api/v2/list_movies.json?genre=western&sort_by=rating&limit=50'},
]

def name():
  return 'YTS Torrents'

def image():
  return 'icon.png'

def description():
  return "YTS Torrents Channel (<a target='_blank' href='https://yts.to'>https://yts.to</a>)."

def feedlist():
  return _FEEDLIST

def feed(idx):
  data = get_json(_FEEDLIST[idx]['url'], proxy=True)
  return _extract(data)

def search(q):
  params = {'query_term':q, 'limit':50}
  data = get_json(_SEARCH_URL, params=params, proxy=True)
  return _extract(data)

def _extract(data):
  rtree = data['data']['movies']
  results = PlayItemList()
  for r in rtree:
    title = r['title_long']
    img = r['medium_cover_image']
    torrent = _smallest_size(r['torrents'])
    url = torrent['url']
    size = torrent['size']
    seeds = torrent['seeds']
    peers = torrent['peers']
    subtitle = chanutils.torrent.subtitle(size, seeds, peers)
    imdb = "<a target='_blank' href='http://www.imdb.com/title/" + r['imdb_code'] + "/'>IMDB Rating: " + str(r['rating']) + "</a>"
    synopsis  = imdb
    subs = movie_title_year(title)
    results.add(TorrentPlayItem(title, img, url, subtitle, synopsis, subs))
  return results

def _smallest_size(torrlist):
  size = torrlist[0]['size_bytes']
  torrent = torrlist[0]
  for t in torrlist:
    if t['size_bytes'] < size:
      size = t['size_bytes']
      torrent = t
  return torrent
