# JournaLog App
- Djangoで作成したジャーナル管理アプリです。
- 1日の振り返りをデジタルで記録することを目的としています。

## 作った背景
- 日頃からノートにアナログで自分の目標とその日やることとスケジュールを記録していたのですがデジタルにしたらどうだろうと思い、制作を始めました

## 主な機能
- ジャーナルの作成 / 編集 / 削除
- 日付ごとのジャーナル管理
- Todo / Goal との連携
- スケジュール管理 / その日の出来事を振り返る機能の実装

## 説明
1. ログインを行います。
2. カレンダーが表示されるので記録したい日付を選択してください。
3. Goal(現在の自分の目標)とTodo(Goalを踏まえた今日やるべきこと)を設定し、保存してください。
4. 保存後の画面で下にスクロールするとSchedule(時間割)の出てくるのでスケジュール管理をしたい場合はタイトルと時刻を入力してください。
5. さらに下に行くとReflection(振り返り)があるので任意記入。(未実装)

## 使用技術
- Python 3.12
- Django 6.0
- SQLite3(MySQLに移行する予定)
- Bootstrap 5

## 今後の改善
- [x] 他のユーザーが投稿したJournalを見れないように制限を実装する
- [x] スマホで気軽に管理できるようにしたいのでレスポンシブ対応を行う
- [x] タスクの完了/未完了の制御の部分を実装する。
- [ ] カレンダー画面からGoalのtitleを確認できるように改善する。
- [ ] journal内にその日の気分や出来事を記録するテキストフォームを追加する。
- [x] 投稿追加画面のところでも複数追加をできるようにする
- [x] homeで月毎表示の時に予定が入っている日の表示を見やすくする。
- [ ] schedule(予定を管理する)機能を追加する。
- [ ] Reflection(振り返り)機能を追加する。


## セットアップ方法

```bash
git clone https://github.com/karuhito/JournaLog_app.git
cd JournaLog_app
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver