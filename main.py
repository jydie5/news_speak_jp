import streamlit as st
#import io
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, AudioConfig
import os
import requests

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

# st.title("=====News Echoes: The Sound of Today's World=====")
# st.header("/////Unraveling World Stories in Audio/////")

#st.markdown('<div class="earth"></div>', unsafe_allow_html=True)
#st.markdown('<div class="header-text">/////Unraveling World Stories in Audio/////</div>', unsafe_allow_html=True)
st.markdown('<h2><span class="header-text"><div class="earth"></div>News Echoes: The Sound of Today\'s World<br>Unraveling World Stories in Audio</span></h2>', unsafe_allow_html=True)
st.write(' ')



# Azureサブスクリプションキーとサービスリージョンを設定
subscription_key = os.environ['AZURE_KEY']
service_region = "japaneast"
# SpeechConfigオブジェクトを作成
speech_config = SpeechConfig(subscription=subscription_key, region=service_region)



#deeplに持ってゆく関数
def translate(text):
    url_deep = "https://api-free.deepl.com/v2/translate"
    params_deep = {
        "auth_key": os.environ['DEEPL_API'],
        "text": text,
        "source_lang": "EN",
        #"target_lang": "ZH"
        "target_lang": "JA" 
        }
    response_deep = requests.post(url_deep, data=params_deep)
    if response_deep.status_code == 200:
        return response_deep.json()["translations"][0]["text"]
    else:
        return None

# NewsAPIのエンドポイントとパラメータを指定する
url = 'https://newsapi.org/v2/top-headlines'
params = {
    'country': 'us',
    'apiKey': os.environ['NEWS_API'],
    'pageSize': '7'
}

# NewsAPIにリクエストを送信する
response = requests.get(url,params=params)

# レスポンスのJSONデータを取得する
data = response.json()


#ssml関数生成
def create_ssml(text, rate='-1%', pitch='+0st', volume='medium'):
    return f'<speak version="1.0" \
        xmlns="https://www.w3.org/2001/10/synthesis" xml:lang="en-US">\
        <voice name="en-US-SaraNeural">\
        <prosody rate="{rate}" pitch="{pitch}" volume="{volume}">{text}</prosody>\
        </voice>\
        </speak>'




def show_and_speak_article(article):
    st.write(f"# {article['title']}")
    st.write(translate(article['title']))
    text = article['title']
    if text:
        ssml = create_ssml(text, rate='slow')

        # 音声出力の設定
        audio_output = AudioConfig(filename="output_audio.wav")

        # SpeechSynthesizerオブジェクトを作成
        synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_output)

        # SSMLから音声を生成
        synthesizer.speak_ssml_async(ssml).get()

        # 生成された音声ファイルを読み込み、Streamlitで再生
        audio_bytes = open("output_audio.wav", "rb").read()
        st.audio(audio_bytes, format="audio/wav")
   

    st.write(f"# {article['description']}")
    st.write(translate(article['description']))
    text = article['description']
    if text:
        ssml = create_ssml(text, rate='slow')

        # 音声出力の設定
        audio_output = AudioConfig(filename="output_audio.wav")

        # SpeechSynthesizerオブジェクトを作成
        synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_output)

        # SSMLから音声を生成
        synthesizer.speak_ssml_async(ssml).get()

        # 生成された音声ファイルを読み込み、Streamlitで再生
        audio_bytes = open("output_audio.wav", "rb").read()
        st.audio(audio_bytes, format="audio/wav")
    st.write('==========================================')




# セッションステートに記事インデックスを初期化
if 'article_index' not in st.session_state:
    st.session_state.article_index = 0

# ボタンが押されるまで待機
if st.button('Voice of the Globe'):
    # 現在の記事インデックスで記事を表示
    show_and_speak_article(data['articles'][st.session_state.article_index])

    # 記事インデックスを更新
    st.session_state.article_index += 1

    # インデックスが記事数を超えた場合、リセット
    if st.session_state.article_index >= len(data['articles']):
        st.session_state.article_index = 0


