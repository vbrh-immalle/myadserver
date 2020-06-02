import sqlite3
from viewmodels import Ad, ResellerInfo, CeoResellerInfo

class AdNotFound(Exception):
    pass

class Db:
    def __init__(self, db_file='./db/myadserver.sqlite3'):
        self.db = sqlite3.connect(db_file)

    def get_aantal_resellers(self):
        qry = self.db.execute('''
            SELECT *
            FROM Reseller
            ''')
        return len(qry.fetchall())

    def get_aantal_ads(self):
        qry = self.db.execute('''
            SELECT *
            FROM Ad
            ''')
        return len(qry.fetchall())

    def get_ad(self, ad_id):
        qry = self.db.execute('''
            SELECT afbeelding, link
            FROM Ad
            WHERE id = ?
            ''', (ad_id,))
        
        row = qry.fetchone()
        if row == None:
            raise AdNotFound

        ad = Ad(
            row[0],
            row[1],
        )
                
        return ad

    def get_reseller_stats(self, reseller_id):
        qry = self.db.execute('''
            SELECT afbeelding, link, aantal_views, aantal_clicks, ROUND(aantal_clicks*1.0/aantal_views, 2) as CTR
            FROM ResellerAd
            JOIN Reseller
              ON Reseller.id = ResellerAd.reseller_id
            JOIN Ad
              ON Ad.id = ResellerAd.ad_id
            WHERE Reseller.id = ?;
            ''', (reseller_id,))

        lines = []
        for row in qry:
            lines.append(ResellerInfo(
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
            ))
        return lines

    def get_ceo_stats(self):
        qry = self.db.execute('''
            SELECT naam as reseller, afbeelding, link, aantal_views, aantal_clicks, ROUND(aantal_clicks*1.0/aantal_views, 2) as CTR
            FROM ResellerAd
            JOIN Reseller
              ON Reseller.id = ResellerAd.reseller_id
            JOIN Ad
              ON Ad.id = ResellerAd.ad_id
            ''')

        lines = []
        for row in qry:
            lines.append(CeoResellerInfo(
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[5]
            ))
        return lines

    def get_ad_from(self, reseller_id, ad_id):
        qry = self.db.execute('''
            SELECT afbeelding, link
            FROM ResellerAd
            JOIN Reseller
              ON Reseller.id = ResellerAd.reseller_id
            JOIN Ad
              ON Ad.id = ResellerAd.ad_id
            WHERE Reseller.id = ? AND Ad.id = ?
            ''', (reseller_id, ad_id))

        row = qry.fetchone()
        if row == None:
            raise AdNotFound

        return Ad(
                row[0],
                row[1],
            )

    def update_views(self, reseller_id, ad_id):
        qry = self.db.execute('''
            UPDATE ResellerAd
            SET aantal_views = aantal_views + 1
            WHERE reseller_id = ? AND ad_id = ?;
            ''', (reseller_id, ad_id))
        self.db.commit()

    def update_clicks(self, reseller_id, ad_id):
        qry = self.db.execute('''
            UPDATE ResellerAd
            SET aantal_clicks = aantal_clicks + 1
            WHERE reseller_id = ? AND ad_id = ?;
            ''', (reseller_id, ad_id))
        self.db.commit()

    def reset_all_counters(self):
        qry = self.db.execute('''
            UPDATE ResellerAd
            SET aantal_views = 0, aantal_clicks = 0
            ''')
        self.db.commit()







if __name__ == "__main__":
    db = Db()
    ad = db.get_ad(1)
    print(ad)
    #print(db.get_ads_from(1))