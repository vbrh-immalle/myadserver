import pytest
import shutil
import db
import viewmodels


@pytest.fixture
def setup_test_db():
    shutil.copyfile(
        './db_test/myadserver_src.sqlite3',
        './db_test/myadserver.sqlite3')

def get_test_db():
    return db.Db('./db_test/myadserver.sqlite3')
    
def test_get_aantal_resellers():
    db = get_test_db()
    assert db.get_aantal_resellers() == 2

def test_get_aantal_ads():
    db = get_test_db()
    assert db.get_aantal_resellers() == 2

def test_get_ad():
    db = get_test_db()
    ad = db.get_ad(1)
    ad_expected = viewmodels.Ad("ad1.png", "http://www.ad1company.com")
    assert ad == ad_expected

def test_get_ad_exception():
    db = get_test_db()
    # TODO
    with pytest.raises(Exception) as e:
        ad = db.get_ad(3)
        assert e.type is db.AdNotFound


def test_get_reseller_stats():
    db = get_test_db()
    ads = db.get_reseller_stats(1)
    ads_expected = [
        viewmodels.ResellerInfo("ad1.png", "http://www.ad1company.com", 0, 0, None),
        viewmodels.ResellerInfo("ad2.png", "http://www.ad2company.com", 0, 0, None)
    ]
    assert ads == ads_expected

def test_get_ceo_stats():
    db = get_test_db()
    ads = db.get_ceo_stats()
    ads_expected = [
        viewmodels.CeoResellerInfo("jos", "ad1.png", "http://www.ad1company.com", 0, 0, None),
        viewmodels.CeoResellerInfo("jos", "ad2.png", "http://www.ad2company.com", 0, 0, None),
        viewmodels.CeoResellerInfo("jan", "ad1.png", "http://www.ad1company.com", 0, 0, None)
    ]
    assert ads == ads_expected

def test_get_ad_from():
    db = get_test_db()
    ad = db.get_ad_from(1, 1)
    ad_expected = ad_expected = viewmodels.Ad("ad1.png", "http://www.ad1company.com")
    assert ad == ad_expected

def test_update_views_and_clicks():
    db = get_test_db()
    ads = db.get_reseller_stats(1)
    ads_expected = [
        viewmodels.ResellerInfo("ad1.png", "http://www.ad1company.com", 0, 0, None),
        viewmodels.ResellerInfo("ad2.png", "http://www.ad2company.com", 0, 0, None)
    ]
    assert ads == ads_expected

    db.update_views(1,1)
    ads_expected[0].aantal_views += 1
    ads_expected[0].CTR = 0.0
    assert ads == ads_expected

    db.update_views(1,1)
    ads_expected[0].aantal_views += 1
    assert ads == ads_expected

    db.update_clicks(1,1)
    ads_expected[0].aantal_clicks += 1
    ads_expected[0].CTR = 0.5
    assert ads == ads_expected


