# sfmon
ソーラーフロンティアモニター ホームサーバダイレクト表示

## About sfmon
ソーラーフロンティアモニターのリアルタイム表示をホームサーバーより直接取得しWeb表示します。

ホームサーバー, SF2MHS-1001
https://www.solar-frontier.com/jpn/products/manual.html

ソーラーフロンティアのフロンティアモニター
ホームエネルギーモニタリングサービス
https://www.frontier-monitor.com/persite/top


## Usage
1.ホームサーバダイレクト表示
■実行環境
Apache mod_wsgi
Python3

------------------------------------------------
Windows11での環境構築例：
PowerShell
Linux環境のインストール（ubuntu）
> wsl --install

Webサーバのインストール
$ sudo apt install apache2
$ sudo apt install libapache2-mod-wsgi-py3

------------------------------------------------
mod_wsgiの設定をインストール

定義をコピー
$ sudo cp wsgi.conf /etc/apache2/conf-available/.

定義を有効化
$ a2enconf wsgi
$ systemctl reload apache2

------------------------------------------------
ホームサーバのIPアドレス設定
app.wsgiの最初の行へホームサーバのIPアドレスを設定する
IP_ADDRESS='192.168.0.xxx'

※ホームサーバやルータの設定でIPアドレス固定にしておくと良いです。

------------------------------------------------
コンテンツのインストール
$ sudo cp -r css images /var/www/html/
$ sudo cp -r wsgi /var/www/

------------------------------------------------
■格納場所確認
$ tree /var/www/
/var/www/
├── html
│   ├── css
│   │   └── rt_import.css
│   ├── images
│   │   ├── auto_off.png
│   │   ├── auto_on.png
│   │   ├── common
│   │   │   └── pop_bg.jpg
│   │   └── manu_in.png
│   └── index.html
└── wsgi
    └── app.wsgi


以下にアクセスして表示されればOK
http://localhost/py

------------------------------------------------
おまけ：画像ファイルの差し替え
フロンティアモニターにログインして以下画像をダウンロードして差し替えれば、見慣れた表示になります。
https://www.frontier-monitor.com/persite/images/common/pop_bg.jpg
https://www.frontier-monitor.com/persite/images/manu_in.png
https://www.frontier-monitor.com/persite/images/auto_on.png
https://www.frontier-monitor.com/persite/images/auto_off.png


