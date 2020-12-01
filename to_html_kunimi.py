from bs4 import BeautifulSoup
from urllib import request
import csv
import pandas as pd



url = 'https://tenki.jp/forecast/9/47/8320/44214/'
response = request.urlopen(url)
soup = BeautifulSoup(response)
soup.find_all()
wether=soup.select(".weather-telop")
rain=soup.select(".rain-probability")
info1=[wether[0],rain[0]]
info2=[wether[1],rain[1]]
csvlist=[["今日の天気"," "],[wether[0].text,rain[0].text],["明日の天気"," "],[wether[1].text,rain[1].text]]
f=open("kunimi.csv","w",encoding="cp932")
writecsv = csv.writer(f, lineterminator='\n')
writecsv.writerows(csvlist)

f.close()

df = pd.read_csv('kunimi.csv',encoding='cp932')
df = df.dropna(axis=1, how='any')

# <th>内の文字列を真ん中に寄せる
pd.set_option('colheader_justify', 'center')

html_string = '''
<html>
  <head><meta charset="cp932">
  <title>国見の天気</title>
  </head>
  <link rel="stylesheet" type="text/css" href="mystyle.css"/>
  <body>
  <header> <!--ページ遷移ボタンを作成-->
        <div class="home">
            <h1 class="home_a">
                <a href="top.html"><img src="img/小麦.png" alt="AGRI"></a>
            </h1>

                    <ul id="nav">
                        <li class="botton"><a href="top.html" vertical-align>Home</a></li>
                        <li class="botton"><a href="top.html">About</a></li>
                        <li class="botton"><a href="area.html">Area</a></li>
                        <li class="botton"><a href="comment.html">Comment</a></li>
                        <li class="botton"><a href="weather.html">Weather</a></li>
                    </ul>
        </div>
    </header>
    {table}
    <b1>降水確率は左から0-6時,6-12時,12-18時,18-24時です</b1>
    <footer>
        <ul id="nav_footer">
              <li><a href="top.html">Home</a></li>
              <li><a href="about.html">About</a></li>
              <li><a href="area.html">Area</a></li>
              <li><a href="comment.html">Comment</a></li>
              <li><a href="#">Weather</a></li>
        </ul>
    </footer>
  </body>
</html>
'''
df = df.replace('\r\n',' ', regex=True)
# OUTPUT AN HTML FILE
with open('kunimi.html', 'w') as f:
    f.write(html_string.format(table=df.to_html(classes='mystyle', index=False)))

