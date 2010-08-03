
from web2con.services import Twitter, TwitterXml, Soundcloud

def test_twitter_public_timeline():
    t = Twitter()
    r = t.statuses.public_timeline()
    assert r
    assert r.headers
    assert r[0]

def test_twitter_public_timeline_xml():
    t = TwitterXml()
    r = t.statuses.public_timeline()
    assert r
    assert r.headers

def test_soundcloud_tracks():
    s = Soundcloud()
    r = s.tracks()
    assert r
    assert r.headers
    assert r[0]
    print r

