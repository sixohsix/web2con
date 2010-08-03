
from web2con.services import Twitter

def test_twitter_public_timeline():
    t = Twitter()
    r = t.statuses.public_timeline()
    assert r
