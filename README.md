# JournaLog App
- Djangoで作成したジャーナル管理アプリです。
- 1日の振り返りをデジタルで記録することを目的としています。

## 作った背景
- 日頃からノートにアナログでその日やることとスケジュールを記録していたのですがデジタルにしたらどうだろうと思い、制作を始めました

## 主な機能
- ジャーナルの作成 / 編集 / 削除
- 日付ごとのジャーナル管理
- Todo / Goal との連携（予定）

## 説明
- ログインを行う。
- カレンダーが表示されるので記録したい日付を選択する。
- Goal(その日やること)とTodo(スケジュール)を設定し、保存する。
## 使用技術
- Python 3.12
- Django 6.0
- SQLite3(MySQLに移行する予定)
- Bootstrap 5

## 今後の改善
- 他のユーザーが投稿したJournalを見れないように制限を実装する
- スマホで気軽に管理できるようにしたいのでレスポンシブ対応を行う
- タスクの完了/未完了の制御の部分を実装する。
- カレンダー画面からGoalのtitleを確認できるように改善する。
- journal内にその日の気分や出来事を記録するテキストフォームを追加する。
- 追加画面のところでも複数追加をできるようにする
## セットアップ方法

```bash
git clone https://github.com/karuhito/JournaLog_app.git
cd JournaLog_app
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver