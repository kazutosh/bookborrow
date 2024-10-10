# 起動方法

## ローカル
開発時はローカルで作業することもできます。
ローカルでの開発はDev Containerをおすすめしますが、Docker Compose単体でも可能です。

### Dev Container
VSCodeにDev Container拡張機能をインストールします。
VSCodeからこのディレクトリを開き、Ctrl+Pを押下し「Dev Container: Reopen in container.」を選択します。
ブラウザで `http://127.0.0.1:5000/` でアプリにアクセスできます

### Docker Compose
ローカルでアプリを起動するには以下のコマンドを実行します（Dockerが必要です）。
```
docker compose up -d
```
コマンド実行後、以下のログが表示後ブラウザで `http://127.0.0.1:5000/` でアプリにアクセスできます
```
app-1  |  * Debug mode: on
app-1  | WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
app-1  |  * Running on all addresses (0.0.0.0)
app-1  |  * Running on http://127.0.0.1:5000
app-1  |  * Running on http://172.20.0.3:5000
```

# 仮想環境のセットアップ
Docker Composeのみで開発する際にVSCode上でコード補完機能を利用するには以下のコマンドを実行します。
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
