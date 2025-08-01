# 必要なライブラリをインポートします
import discord

# --- 設定項目 ---
# 自分のボットのトークンに置き換えてください
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# 自己紹介を投稿させたいチャンネルのIDに置き換えてください
# ここに「#自己紹介」チャンネルのIDを設定します
SELF_INTRODUCTION_CHANNEL_ID = 1177232123770450020

# ▼▼▼ ここにキーワードと返信するリンクやメッセージを追加・編集してください ▼▼▼
KEYWORD_LINKS = {
    "公式": "https://www.pokemon-card.com/",
    "ルール": "https://www.pokemon-card.com/assets/document/rules/floor-rule_20250131.pdf",
    "デッキ": "https://www.pokemon-card.com/deck/",
    "カード検索": "https://www.pokemon-card.com/card-search/index.php?keyword=&se_ta=&regulation_sidebar_form=XY&pg=&illust=&sm_and_keyword=true",
    "大会結果": "https://players.pokemon-card.com/event/result/list"
}
# ▲▲▲ ここまで ▲▲▲
# ----------------

# ボットがさまざまな操作を行えるようにするための設定（インテント）
intents = discord.Intents.default()
intents.message_content = True

# ボットのクライアント（本体）を作成します
client = discord.Client(intents=intents)

# ボットが起動したときに実行されるイベント
@client.event
async def on_ready():
    # 起動時の処理をシンプルにしました
    print(f'{client.user} としてログインしました！')
    print('------')
    # 起動時の自己紹介は行わなくなったため、関連コードは削除しました

# メッセージを受信したときに実行されるイベント
@client.event
async def on_message(message):
    # Bot自身のメッセージには反応しないようにします
    if message.author == client.user:
        return

    # 【優先度1】まずBotへのメンションが含まれているか確認します
    if client.user.mentioned_in(message):
        command = message.content.split('>', 1)[-1].strip()

        # --- ▼▼▼ デバッグ用のコード ▼▼▼ ---
        print("--- デバッグ情報 ---")
        print(f"受け取ったコマンド: '[{command}]'")
        print("--------------------")
        # --- ▲▲▲ ここまで ▲▲▲ ---

        if command in KEYWORD_LINKS:
            response = KEYWORD_LINKS[command]
            await message.channel.send(response)
        else:
            await message.channel.send(f"「{command}」には対応していません。")
    # 【優先度2】メンションがなく、かつ「#自己紹介」チャンネルへの投稿だった場合に実行します
    elif message.channel.id == SELF_INTRODUCTION_CHANNEL_ID:
        # Botの自己紹介メッセージを定義します
        intro_message = (
            "おじポケBotです！皆さんの楽しいポケカライフをサポートします。"
            "いろいろ機能を追加していくのでよろしくお願いします！！"
        )
        try:
            # メッセージを送信します
            await message.channel.send(intro_message)
            print(f"#{message.channel.name} に自己紹介メッセージを送信しました。")
        except discord.errors.Forbidden:
            print(f"エラー: #{message.channel.name} にメッセージを送信する権限がありません。")
        except Exception as e:
            print(f"メッセージ送信中に予期せぬエラーが発生しました: {e}")

# ボットを起動します
# ※設定変数の名前を変更したため、ここのチェックも修正しました
if BOT_TOKEN == "ここにあなたのボットのトークンを貼り付け" or SELF_INTRODUCTION_CHANNEL_ID == 0:
    print("エラー: BOT_TOKEN または SELF_INTRODUCTION_CHANNEL_ID が設定されていません。")
    print("コードを編集して、正しい値を設定してください。")
else:
    try:
        client.run(BOT_TOKEN)
    except discord.errors.LoginFailure:
        print("エラー: 不正なトークンです。トークンが正しいか確認してください。")
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")