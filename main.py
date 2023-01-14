from email.utils import decode_rfc2231
from turtle import color
import webbrowser
from xml.dom.expatbuilder import theDOMImplementation
import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import time
from PIL import Image


st.set_page_config(
    page_title="Python初心者によるmlb考察",
    layout="wide",
    menu_items={
        'Get Help':'https://www.google.com/',
        'About':"""
        # 野球好きPython初心者によるデータ分析
        データビジュアライゼーションを中心としたmlbのサイ・ヤング賞についてをまとめました。
        """
    })




##サイドバーの表示
st.sidebar.markdown("## Settings")
st.sidebar.write("ここから使えます。")
url = 'https://streamlit.io/'
if st.sidebar.button("let's go to the streamlit!"):
    webbrowser.open_new_tab(url)

text = st.sidebar.text_input('あなたの感想を教えてください。')
st.sidebar.write('私は', text, 'だと思う。')
##以下本文

graduation_work = "<h1>2022年サイ・ヤング賞予測分析</h1>"
st.components.v1.html("<center>" + graduation_work + "</center>")

##プログレスバーの表示

st.write('準備中...')
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
    latest_iteration.text(f'Iteration {i+1}')
    bar.progress(i + 1)
    time.sleep(0.05)




st.header("1.今回の分析内容とその目的")

column_left, column_right = st.columns(2)
with column_left:
    st.write("野球好きである2人がMLBにおける今年のMVP、サイ・ヤング賞についてをデータから読み取り、予測・比較をしていく。今回は今季最も注目されている大谷翔平とアーロン・ジャッジに特に注目して分析を行なっていく。")
    st.write("また、今回は担当として私がサイ・ヤング賞の予測を行い、MVPは鈴木くんが行うものとする。")
    st.write("ここでは野球のこれまでのデータをもとにした予測分析と、Pythonだけで容易にデザインから多様なウィジェットまで扱うことが可能な「streamlit」の機能性についてを交えて説明していこうと考える。")
with column_right:
    st.image('https://full-count.jp/wp-content/uploads/2022/09/03085148/20220903_ohtani_judge_reu.jpg')
    st.caption("画像:https://full-count.jp/2022/09/12/post1279929/")

container = st.container()
with container:
    st.header("今回用いるフレームワーク")
container.subheader("・streamlit")
container.write("PythonでWEBアプリケーションを作成するためのフレームワークであり、バックエンド開発の知識がなくてもPythonのコードを数行書くだけで、気軽にデモ用のアプリを作成することができるのが特徴である。")


st.header('2.今回用いるデータの紹介')
st.write("今回は2019〜2022年の成績を中心に予測・比較を行なっていく。なお2020年は新型コロナウイルスの影響から試合数が大幅に縮小しての開催のためデータからは除外した。")
##データを表示をボタンで切り替え
dfs = [pd.read_csv('data/Pstats_' + str(yr) + '.csv')for yr in (2019, 2021, 2022)]

col1 = st.columns(3)
show_2019 = col1[0].button('2019year')
show_2021 = col1[1].button('2021year')
show_2022 = col1[2].button('2022year')

if show_2019:
    st.write(dfs[0])
elif show_2021:
    st.write(dfs[1]) 
elif show_2022:
    st.write(dfs[2])

st.caption("引用:https://www.mlb.com/, https://www.baseball-reference.com/")

st.header('3.サイ・ヤング賞の予測')

expander1 = st.expander("サイ・ヤング賞とは？")
expander1.write("The Cy Young Award is given annually to the best pitcher in each league. From its establishment in 1956 until 1966, it was presented to the best pitcher in Major League Baseball. Since 1967, there is one winner from each of the American and National leagues. From 1956 to 1958, a pitcher was not allowed to win the Cy Young Award twice. The Baseball Writers' Association of America (BBWAA) votes on the Cy Young Award at the conclusion of each season before the postseason starts.")
expander1.write("和訳（サイ・ヤング賞は、毎年各リーグの最優秀投手に贈られる。 1956年の設立から1966年まで、メジャーリーグベースボールの最優秀投手に贈られました。 1967 年以来、アメリカン リーグとナショナル リーグのそれぞれから 1 人の勝者がいます。 1956年から1958年まで、投手はサイ・ヤング賞を2度受賞することを許されなかった。 アメリカ野球記者協会 (BBWAA) は、ポストシーズンが始まる前に、各シーズンの終わりにサイ・ヤング賞の投票を行います。）")

st.caption("※参照:https://www.baseball-reference.com/awards/cya.shtml")
expander2 = st.expander("選出基準は？")
expander2.write("選出基準:NPBの沢村賞とは異なり、明確な基準は設けられておらず、記者による「今年1番活躍した投手は誰か」という観点からア・リーグ、ナ・リーグから1人ずづ選出されている。実際に2018年にはナ・リーグにおいてデグロム投手が10勝で選出されている。")

st.subheader('①個人的仮説')
st.write('前述したようにデグロムが勝利数10でサイ・ヤング賞を獲得したように、近年打者成績によって左右されてしまうW(勝利数)は他の指標と比べて重要視されていないと予想する。また近年の投手運用上投手の選手生命を守る投球数の制限を設ける動きが加速しているため、IP(投球数)は大きく評価されるようになってきたのではないかと予想する。投球数に関連してWHIPやAVGといった指標もサイ・ヤング賞に選ばれる上で相乗して好成績者が選ばれるような動きになっていると分析し、予想を立てていく。')

##ラジオボックスでデータ表示
def main():
    selected_item = st.radio('年度を選択してください。',
                             ['2019', '2021', '2022', '表示を消す'])
    if selected_item == '2019':
        df = pd.read_csv('data/Pstats_2019.csv')
        df_columns = df.columns
        x = st.selectbox("X", df_columns)
        y = st.selectbox("Y", df_columns)
        fig = plt.figure(figsize = (12,8))
        plt.scatter(df[x],df[y])
        plt.xlabel(x, fontsize = 18)
        plt.ylabel(y, fontsize = 18)
        st.pyplot(fig)
    elif selected_item == '2021':
        df = pd.read_csv('data/Pstats_2021.csv')
        df_columns = df.columns
        x = st.selectbox("X", df_columns)
        y = st.selectbox("Y", df_columns)
        fig = plt.figure(figsize = (12,8))
        plt.scatter(df[x],df[y])
        plt.xlabel(x, fontsize = 18)
        plt.ylabel(y, fontsize = 18)
        st.pyplot(fig)
    elif selected_item == '2022':
        df = pd.read_csv('data/Pstats_2022.csv')
        df_columns = df.columns
        x = st.selectbox("X", df_columns)
        y = st.selectbox("Y", df_columns)
        fig = plt.figure(figsize = (12,8))
        plt.scatter(df[x],df[y])
        plt.xlabel(x, fontsize = 18)
        plt.ylabel(y, fontsize = 18)
        st.pyplot(fig)

if __name__ == '__main__':
    main()

st.write('上はラジオボタンによって各年の成績の指標をx軸、y軸の組み合わせを自在に変更することが可能な散布図を示した。')
st.write('このようにstreamlitでは与えられたデータから動的なグラフや表など、視覚的に理解しやすいようなwebアプリケーションの作成に優れているということがわかった。')

expander3 = st.expander("各種成績について")
expander3.write("・WAR...WAR（Wins Above Replacement）とは、打撃、走塁、守備、投球を総合的に評価して選手の貢献度を表す指標である。同じ出場機会分を最小のコストで代替可能な控え選手（リプレイスメント・レベルの選手）が出場する場合に比べてどれだけチームの勝利数を増やしたかによって計算される。")
expander3.write("・WHIP...イニングあたりに平均してどれだけ出塁を許したかを表す指標。1.20～1.40程度が平均的で、値が低いほど出塁を許さず安全な投球をしていると評価することができる。計算式はWHIP＝（被安打＋与四球）÷投球回")
st.caption("引用:https://1point02.jp/op/index.aspx")

#ここから2022予測
st.subheader('②サイ・ヤング賞最終候補(11/7時点)')
st.write('11/7に発表された最終候補は、サイ・ヤング賞はD.Cease,A.Manoah,J.Verlanderの3人であった。これに加えて二刀流選手として注目を集めている大谷翔平選手も含めて考察していく。')

df2022 = pd.read_csv('data/Pstats_2022.csv')
st.write(df2022.iloc[[3, 9, 15, 19], :].style.highlight_max(subset=['IP', 'SO'], axis=0).highlight_max(subset=['W','WAR'], color='orange').highlight_min(subset=['ERA', 'AVG', 'WHIP'], color='orange'))

player_list = ['Manoah', 'Cease', 'Varlander', 'Otani']
option = st.selectbox(
    'あなたはどの候補者がサイ・ヤング賞を勝ち取ると思いますか？',
    player_list
)
'あなたの予想は、', option ,'です。'

st.write('色をつけた箇所は最終候補に選ばれた4選手を比較した中で最も優れた成績を残し、<span style="background:yellow">黄色</span>にハイライトした部分は4選手中の最高であり、<span style="background:orange">オレンジ</span>色にハイライトした部分は2022年のアメリカン・リーグの中で最も優れているといったように分類した。', unsafe_allow_html=True)
st.write('読み取れることとして、Varlanderが4項目においてリーグ最高の成績を収めており、4選手の中でも突出していることがわかる。特に日本では投手3冠とも呼ばれる「最多勝利・最優秀防御率・最多奪三振」の中から2冠を達成しており、メジャーリーグ全体においても屈指の投手と呼べることがわかる。')
st.write('一方でManoahは4選手の中では1番多くのイニングを投げ、またWARにおいてもVarlanderと同じ数値を挙げるなど引けを取らないピッチングをできたと言える。Ceaseにおいても三振数が多く、それによってリーグで最も高いWARを挙げチームにとって非常に高い貢献をした選手である。そして日本が誇る大谷選手は最終候補3人の中には残らなかったものの、打者出場との両立もありながら候補選手にも劣らない成績を残し、投手WARにおいてもManoah ,Varlanderより高い数値を挙げるなど選手されても異論はない程の完成度であったと言える。')
st.write('サイ・ヤング賞は指標的な基準は特に存在せず、記者投票によるものなので記者による印象といった部分や球団自体の人気などが少なからず影響されているのではないかと考えた。そこでまずは４選手における被打率の月間成績を取り出し、傑出した月があるかについて調べてみることにした。')

dfVarlander = pd.read_csv('data/Varlanderstats_2022.csv')
dfManoah = pd.read_csv('data/Manoahstats_2022.csv')
dfCease = pd.read_csv('data/Ceasestats_2022.csv')
dfOtani = pd.read_csv('data/Otanistats_2022.csv')

dfmonth2022 = pd.read_csv('data/month_2022.csv')


st.subheader('4選手月間投手成績')
st.line_chart(dfmonth2022)
st.caption("参照：https://www.baseball-reference.com/")

st.write("上のグラフは4選手の月間ごとの被打率を算出したものであるが、各選手の特徴として、")
st.write("Manoah,Otaniはシーズンを通して安定した成績の中で、印象強く被打率が低い月成績を挙げ、また両者とも比較的シーズン後半に成績を良化させていることがわかる。")
st.write("Varlanderはシーズンの中でAVGを.200を超えることが2度しかなく、どの月を見ても4選手の中で最もAVGが高い月がなくシーズンを通して高水準を安定して叩き出していることがわかり、4選手の中で最も「完成された投手」であると言う印象を受けた。")
st.write("Ceaseはシーズン当初こそやや不調気味ではあったものの、4ヶ月連続して.200を下回り、10月の1試合の登板で大幅に悪化してしまったものの私が注目していた記者の印象の部分としては4選手の中では最も存在感を発揮した選手であるとこのグラフから読み取れた。")
st.write("また過去10年間（2020年を除く）ではサイ・ヤング賞に選ばれた選手が所属するチーム成績が地区優勝を果たしている確率は5/10と、味方の援護によって左右する「W」はそれほど重要視されておらず、優勝チームが投票に大きな影響を与えているということは、近年では小さくなっていると考えられる。その背景として近年では様々な指標をもとにして数値から選手を評価する傾向がかなり強まってきており、記者が評価する比較対象が増加したことが影響していると考えられる。")
st.header("③予測結果")
("以上により、記者による印象度合いやこれまでのサイ・ヤング賞に受賞した選手の特徴などから推測すると、今季サイ・ヤング賞を受賞する選手はJ.Varlander選手ではないかと考えました。理由としては、表であげた4項目においてリーグ最高の成績を挙げ、月間成績においてもシーズン序盤に圧倒した成績を残し貴社への強い印象を与えるとともに、地区優勝・ワールドシリーズ制覇に貢献するなど選出に相応しいパフォーマンスを示したと言えるためである。")
("またプレーオフも含めて考えると、ManoahとVarlanderは出場しCeaseが未出場であり、またManoahがワイルドカードシリーズで登板し敗戦投手となり、かたやVarlanderは4試合に登板し2勝を挙げチームはWS制覇するなどVarlanderが最もチームの貢献度が高いと言えるため、これらを含めるとVarlanderに利があると考えられる。")
expander4 = st.expander("mlbにおけるプレーオフの仕組み")
expander4.image("https://no-05.com/wp-content/uploads/2017/09/mlb-playoff-tournament.png")
st.caption("引用:https://no-05.com/mlb-playoff/")
#以下データ分析のコード

'''
tab1, tab2 = st.tabs(["a", "b"])
with tab1:
    st.write("aaa")
'''

st.header("④サイ・ヤング賞受賞者と考察との比較")

col1, col2,col3 = st.columns(3)
with col1:
    st.caption("J.Varlander")
    st.image("https://img.mlbstatic.com/mlb-photos/image/upload/d_people:generic:headshot:67:current.png/w_213,q_auto:best/v1/people/434378/headshot/67/current")

with col2:
    st.caption("A.Manoah")
    st.image("https://img.mlbstatic.com/mlb-photos/image/upload/d_people:generic:headshot:67:current.png/w_213,q_auto:best/v1/people/666201/headshot/67/current")

with col3:
    st.caption("D.Cease")
    st.image("https://img.mlbstatic.com/mlb-photos/image/upload/d_people:generic:headshot:67:current.png/w_213,q_auto:best/v1/people/656302/headshot/67/current")

st.write("2022年のサイ・ヤング賞は11月16日(日本時間17日)に発表され、結果はJ.Varlanderが3年ぶり3度目の受賞を果たした。Varlanderは個人タイトルとして最多勝と最優秀防御率の2冠に輝き、投票結果は万票でのサイ・ヤング賞選出となった。2位にはD.Cease、3位にA.Manoah、そして大谷翔平は4位となっていた。一部記者のコメントによると、")
st.info("「RA9、ファングラフス、ベースボールプロスペクタス、ベースボールレファレンスのWARを複合した上で、Pitching+も若干考慮した上で投票した。」")
st.info("「選手の勝利に対する貢献度を測る指標WARに盲目的に従うことを避けた。」")
st.write("といったコメントが挙げられた。")

vote = pd.read_csv('data/vote.csv')
expander5 = st.expander('投票の内訳')
expander5.table(vote)

st.write('予想との比較については、サイ・ヤング賞受賞者がVaelanderという予想が当たったが、個人的に驚いたのが満票での選出であった点で満票での選出は両リーグ通じて2020年を除いた10年で2人のみで、2011年にVarlanderは満票での選出となり今回で自身2回目と歴代でも指折りの実績を誇る投手となった。')
st.write('また記者からのコメントや実際に6.4で4人中最高であったCeaseではなく5.9であったVarlanderが選出されたことから、様々な指標からの数値的比較に服するのではなく、記者が実際に目で見た選手のパフォーマンスぶりがやはり影響しているのではないかと考える。')

st.header('⑤まとめとstreamlitについて')
st.write('今回Python初心者である私が実際にデータビジュアライゼーション・機械学習を用いて大好きな野球を様々な角度から分析を行いました。今回行ったことよりもさらに高度な分析を取り込み、私たちが応援している目の前で勝利を提供している選手とそれを支えている人々への尊敬の念が一層強まりました。')
columns_left, columns_right = st.columns(2)
with columns_left:
    st.write("""
    データ分析を行うことによって知ることができた野球の魅力について、
    - データの可視化によってあらゆる指標の関わりがわかり、隠れた優秀な選手を評価するなど視点が大きく変わった。
    - 現在は日本、米国とも記者投票によって数字以外の面の影響が考慮される中で、別の視点から選手同士の比較を行うことができる。
    - 野球だけでなく別のスポーツや日常の些細な部分など多くの物事に応用・反映する関心が大いに高まった。
    """)
    

with columns_right:
    st.write("""
    streamlitについての使用感は、
    1. 少ないコードでデータの可視化や様々なウィジェットを用いてわかりやすくデザイン性のあるウェブアプリの製作が可能である。
    1. htmlやcssを利用せずにwebデザインができるため、1から簡単に自身が思い描いたものを制作することが可能である。
    1. htmlやcssの埋め込みも可能なためstreamlitだけでは実現が難しいような部分を補完し合うことが可能であり、個人的にhtml,cssで同じものを制作するよりも負担が少ないと感じた。
    """)

st.write('上記のように紹介したようにstreamlitでのウェブアプリ作成においてまだまだ実現可能なことが多く存在し、制作テーマによって柔軟に使い分けることが可能である。')
    


agreement = st.slider('今回の分析に納得することができましたか？', 0, 100, 50)
'納得度合い:',agreement

