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
  <!--githubからjQueryを取得-->
  <script type="text/javascript" src="https://raw.githubusercontent.com/RikutoTera/to_html_kunimi/jquery-3.5.1.min.js"></script>
  <title>国見の天気</title>
  <script type = "text/javascript">
     $(document).ready(function(){$("#date").load("https://raw.githubusercontent.com/OnoRyota/bungotakada/gh-pages/date.txt");});

  </script>
  </head>
  <link rel="stylesheet" type="text/css" href="mystyle.css"/>
  <body>
  <header> <!--ページ遷移ボタンを作成-->
        <div class="home">
            <h1 class="home_a">
                <a href="top.html"><img src="https://raw.githubusercontent.com/RikutoTera/to_html_kunimi/小麦.png" alt="AGRI"></a>
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
      <!--日付・地域情報を表示-->
  <p id = "date"></p>
<table id="wrap">
  <script>
    <!--変数listに26を代入-->
  	const list = Array.from(new Array(26)).map((v,i) => i)
    $(function(){
      <!--GitHubからjsonファイルを取得-->
      $.getJSON("https://raw.githubusercontent.com/OnoRyota/bungotakada/gh-pages/BungotakadaNoAme.json", function(sample_list){
        <!--要素を一つづつ取り出しテーブルとして表示する-->
        
        for(var i in sample_list){
        	var h = '<tr>'
        	$("table#wrap").append(h);
        	
        	for(var j in list){
          	    h = '<td>'
                + sample_list[i][j]
                + '</td>'
           $("table#wrap").append(h);
          }
          h = '</tr>'
          $("table#wrap").append(h);
        }
        
      });
    });
  </script>
</table>

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

