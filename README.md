# Journal App

Djangoで作成したジャーナル管理アプリです。
1日の振り返りをデジタルで記録することを目的としています。

## 主な機能
- ジャーナルの作成 / 編集 / 削除
- 日付ごとのジャーナル管理
- Todo / Goal との連携（予定）

## 使用技術
- Python 3.12
- Django 6.0
- SQLite3(MySQLに移行する予定)

## セットアップ方法

```bash
git clone https://github.com/karuhito/JournaLog_app.git
cd JournaLog_app
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver