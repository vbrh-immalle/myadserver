import pytest
import os
from db import Db
import viewmodels
import sqlite3

TESTDB_PATH = 'myadserver_testdb.sqlite3'

@pytest.fixture
def test_db_path():
    print(f'Creating test db [{TESTDB_PATH}]...')
    try:
        os.remove(TESTDB_PATH)
    except OSError:
        pass
    tmpdb = sqlite3.connect(TESTDB_PATH)
    tmpdb.executescript('''
        CREATE TABLE "Ad" (
            "id"	INTEGER,
            "afbeelding"	TEXT,
            "link"	TEXT,
            PRIMARY KEY("id")
        );
        
        CREATE TABLE "Reseller" (
            "id"	INTEGER,
            "naam"	TEXT,
            PRIMARY KEY("id")
        );

        CREATE TABLE "ResellerAd" (
            "id"	INTEGER,
            "reseller_id"	INTEGER,
            "ad_id"	INTEGER,
            "aantal_views"	INTEGER,
            "aantal_clicks"	INTEGER,
            PRIMARY KEY("id")
        );

        INSERT INTO "Ad" (id, afbeelding, link)
        VALUES 
            (1, "ad1.png", "http://www.ad1company.com"),
            (2, "ad2.png", "http://www.ad2company.com");

        INSERT INTO "Reseller" (id, naam)
        VALUES
            (1, "jos"),
            (2, "jan");

        INSERT INTO "ResellerAd" (id, reseller_id, ad_id, aantal_views, aantal_clicks)
        VALUES
            (1, 1, 1, 0, 0),
            (2, 1, 2, 0, 0),
            (3, 2, 1, 0, 0);
    ''')
    tmpdb.close()
    return TESTDB_PATH
    
def test_get_aantal_resellers(test_db_path):
    db = Db(test_db_path)
    assert db.get_aantal_resellers() == 2

def test_get_aantal_ads(test_db_path):
    db = Db(test_db_path)
    assert db.get_aantal_resellers() == 2

def test_get_ad(test_db_path):
    db = Db(test_db_path)
    ad = db.get_ad(1)
    ad_expected = viewmodels.Ad("ad1.png", "http://www.ad1company.com")
    assert ad == ad_expected

def test_get_ad_exception(test_db_path):
    db = Db(test_db_path)
    # TODO
    # with pytest.raises(Exception) as e:
    #     ad = db.get_ad(3)
    #     assert e.type is db.AdNotFound


def test_get_reseller_stats(test_db_path):
    db = Db(test_db_path)
    ads = db.get_reseller_stats(1)
    ads_expected = [
        viewmodels.ResellerInfo("ad1.png", "http://www.ad1company.com", 0, 0, None),
        viewmodels.ResellerInfo("ad2.png", "http://www.ad2company.com", 0, 0, None)
    ]
    assert ads == ads_expected

def test_get_ceo_stats(test_db_path):
    db = Db(test_db_path)
    ads = db.get_ceo_stats()
    ads_expected = [
        viewmodels.CeoResellerInfo("jos", "ad1.png", "http://www.ad1company.com", 0, 0, None),
        viewmodels.CeoResellerInfo("jos", "ad2.png", "http://www.ad2company.com", 0, 0, None),
        viewmodels.CeoResellerInfo("jan", "ad1.png", "http://www.ad1company.com", 0, 0, None)
    ]
    assert ads == ads_expected

def test_get_ad_from(test_db_path):
    db = Db(test_db_path)
    ad = db.get_ad_from(1, 1)
    ad_expected = ad_expected = viewmodels.Ad("ad1.png", "http://www.ad1company.com")
    assert ad == ad_expected

def test_update_views_and_clicks(test_db_path):
    db = Db(test_db_path)
    ads = db.get_reseller_stats(1)
    ads_expected = [
        viewmodels.ResellerInfo("ad1.png", "http://www.ad1company.com", 0, 0, None),
        viewmodels.ResellerInfo("ad2.png", "http://www.ad2company.com", 0, 0, None)
    ]
    assert ads == ads_expected

    db.update_views(1,1)
    ads = db.get_reseller_stats(1)
    ads_expected[0].aantal_views += 1
    ads_expected[0].CTR = 0.0
    assert ads == ads_expected

    db.update_views(1,1)
    ads = db.get_reseller_stats(1)
    ads_expected[0].aantal_views += 1
    assert ads == ads_expected

    db.update_clicks(1,1)
    ads = db.get_reseller_stats(1)
    ads_expected[0].aantal_clicks += 1
    ads_expected[0].CTR = 0.5
    assert ads == ads_expected
