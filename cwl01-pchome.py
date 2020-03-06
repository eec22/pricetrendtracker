import requests
import json
import sqlite3

conn = sqlite3.connect('C:\\cwl.db', timeout=20)  # 連接資料庫 db
cur = conn.cursor()  # 創一個cursor物件

for i in range(1, 30):
    url = f"https://ecshweb.pchome.com.tw/search/v3.3/all/results?q=顯示卡&page={i}&sort=sale/dc"
    res = requests.get(url)
    data = json.loads(res.text)
    prods = data['prods']
    # print(prods)
    for news in prods:
        keyid = news['Id']
        name = news['name']
        price = news['price']
        cur.execute("insert into prod_vga(keyid, pname, regdate, price) values(?,?,DATE('now','localtime'),?)",
                    (keyid, name, price))
        #建立一個時間
        conn.commit()
        #在這邊提交是為了防止連續連線讓系統產生訊息，訊息會造成辨識失敗，這邊先提交可以避免寫入沒有完成
    # cur.execute("DELETE FROM prod_vga WHERE id not like 'DRAD%'")
    # 刪除其他非目標分類
    # 有機會刪到不應該刪的
    # 資料庫格式還有待修改

#有機會出現JSON查詢錯誤失敗之類的狀況，但是是因為出現"系統忙碌中，請稍後在試..."的錯誤訊息，所以被判定錯誤，
#但是在迴圈內就Commit的話就算出現錯誤資料也已經寫入，出現錯誤無妨
conn.commit()
conn.close()