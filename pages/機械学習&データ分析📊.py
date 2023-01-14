import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px

st.header('機械学習による2022年度の実質的なサイ・ヤング賞受賞者')
tab1, tab2 = st.tabs(["考察1", "考察2"])
with tab1:
    st.write('今回は私がリーグの中でも最優秀選手に選ばれるために最も重要であると考えている「ERA, IP, SO, WHIP, AVG」を説明変数として設定し、「CYA」を目的変数としてLogisticRegressionによって2022年度の成績から誰がサイ・ヤング賞に相応しいかを導き出してみようと考えた。')

    st.subheader('0.用いるデータの説明')
    ('今回機械学習を行うために用いるデータは2012〜2022分のデータを用いて分析を行う。（2020はコロナウイルスの影響で試合数が少なく、極端に他の年度とデータの数値に違いがあるため今回は除外。）')

    st.subheader('1.必要モジュールのインポート')
    ('まずは機械学習に必要なモジュールのインストールを行う。今回は以下のものをインポートする。')
    st.code('import numpy as np\nimport pandas as pd\nfrom sklearn.linear_model import LogisticRegression')

    st.subheader('2.データを読み込みデータフレームに変換する。')
    code1 = '''dfs = [pd.read_csv('data/Pstats_' + str(yr) + '.csv') for yr in (2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2021, 2022)]'''
    st.code(code1, language='Python')

    st.subheader('3.各年のデータを一つにまとめる。')
    code2 = '''whole_year_array = np.concatenate(dfs[:10], axis = 0)'''
    ('2012〜2022の各データを一つにまとめ、whole_year_arrayに代入する。')
    st.code(code2, language='Python')

    st.subheader('4.DataFrameを作成する。')
    ('3でまとめたデータをpandasを用いてdataframeを作成し、df_whole_yearに代入。')
    code3 = '''df_whole_year = pd.DataFrame(data = whole_year_array, columns = dfs[0].columns)'''
    st.code(code3, language='Python')

    st.subheader('5.説明変数、目的変数の設定')
    code4 = '''x_train = df_whole_year[['ERA', 'IP', 'SO', 'WHIP', 'AVG']]\ny_train = df_whole_year[['CYA']]\ny_train = y_train.astype('int')\nx_test = dfs[9][['ERA', 'IP', 'SO', 'WHIP', 'AVG']]\ny_test = dfs[9][['CYA']]\ny_test = y_test.astype('int')'''
    ('特徴量をx_trainにdf_whole_yearのERA, IP, SO, WHIP, AVGの5要素を代入。正解データはy_trainにCYAを代入する。そしてLogisticRegressionを行うためにデータ型をint型に変換する。')
    ('そしてテストデータを設定すると、同様にテストデータのデータ型もint型に変換する。')
    st.code(code4, language='Python')

    st.subheader('6.分析結果')
    code5 = '''model = LogisticRegression()\nmodel.fit(x_train, y_train)\nmodel.predict(x_test)'''
    st.code(code5, language='Python')
    ('LogisticRegressionによって評価した結果、今年のキャリアではサイ・ヤング賞に相応しい選手が見当たらないという結果となってしまった。')
    st.code('array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])')
    ('モデルの正解率は以下のように0.954545...という結果であった。')
    st.code('model.score(x_test, y_test)\n0.9545454545454546')

    st.subheader('7.修正')
    code7 = '''x_train = df_whole_year[['W', 'ERA', 'WHIP', 'AVG']]\nx_test = dfs[9][['W', 'ERA', 'WHIP', 'AVG']]'''
    ('分析した結果、サイ・ヤング賞が0人という結果になってしまったため次は説明変数を変更して行なった結果以下のように出力された。')
    st.code('array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0])')
    ('ここで16行目の選手を見るとJ.Varlanderとなっており、説明変数についてW , ERA , WHIP , AVGと変更することで誰が2022のCYAに相応しいかを導出することができた。')

with tab2:
    st.header('WARを中心とした考察')
    st.write('ここでは勝利に対しての貢献度を計る"WAR"を中心に話を進めていく。WARとは本来プレーの中では見えにくいような勝利への貢献度合いを数値化したものであるため、選手の能力に対する評価を行う上で欠かせないものとなっている。また記者によるコメントからも、サイ・ヤング賞を選出する上でWARが中心的な指標となっているのではないかと考えWARについて念頭に置いて分析を行っていくものとする。')
    st.write('まずは2012〜2022の規定投球回到達者のWARについて平均値は2.8506756756756753となり、中央値は2.6500000000000004という結果となった。その差がおよそ0.2でありほとんど差がないことから正規分布に近いと言うことが読み取れる。')
    code6 = '''print(df_whole_year['WAR'].mean())\nprint(df_whole_year['WAR'].median())'''
    st.code(code6, language='Python')

    st.markdown("また2012〜2021までにCYAを獲得した選手のみを抽出し、WARの平均値と中央値を導出したところ平均値は **_6.822_** 、中央値が **_6.6_** という結果であった。また当期間でCYAのWARの最低値は2016の **_4.7_** であり、この年はVarlanderが7.4と飛び抜けた成績であったのにも関わらずの選出のため大きな話題となった。")
    st.write('今年の候補3選手は5.9、5.9、6.4と例年よりは数値が低いもののどの選手もひしめき合っているため、3選手全員にチャンスがあったことがわかった。')

    st.write('度数分布表からヒストグラムを作成し、結果は以下のような形を示した。2012-2021は若干左に偏りがあるが比較的左右対称であり、今回階級幅を0.2とし、最頻値は3.4〜3.6の区間であった。2022は2012-2021と比較すると、7以上が存在せず飛び抜けた投手が存在しなかったことがわかる。ただ-1を切る選手がいないなど全体を通して平均にまとまったのが2022であるといったことが読み取れる。')

    ##以下2012〜2022と2022のヒストグラフ
    col1, col2 = st.columns(2)
    with col1:
        st.image('2012-2021war.png', '2012-2021のWAR')
    with col2:
        st.image('2022war.png', '2022のWAR')
    
    st.write('')
    st.write('またWARについてさらにわかりやすく可視化するために、WARをx軸において様々な指標との関係性について「plotly express」を用いてグラフ化した。データは2022シーズンのものである。グラフを見てわかる通り、WARはWHIP,AVGが比較的大きな負の相関を示していることがわかる。WARとの相関係数はIPが0.553...、WHIPは-0.670...、AVGは-0.828...であった。サイ・ヤング賞にも大きな影響を与えるWARはIPを多くするよりもWHIP、AVGなど各打者を制圧していく能力を高めていくことがより重要な要素になっていることがわかる。Varlanderにおいても今季はWHIP、AVGがリーグトップであり、Ceaseと試合数が4試合も離れているのに対してWARの差が0.5ほどしかないため、これらの指標が評価されているのではないかと予測できる。')

    option = st.selectbox(
        'select',
        ('WAR & IP', 'WAR & WHIP', 'WAR & AVG'))
    if option == 'WAR & IP':
        df = pd.read_csv('data/Pstats_2022.csv')
        df2022 = pd.DataFrame(data = df,columns = df.columns)

        fig1 = px.scatter(
            df2022,
            x = 'WAR',
            y = 'IP',
            text = 'PLAYER',
            color = 'TEAM',
            size_max=30,
            height=500,
            width=800,
            size = 'W',
            color_discrete_map={
               'BOS' : '#c03832',
               'NYY' : '#cb483e',
               'TB' : '#01013b',
               'TOR' : '#436599',
               'BOL' : '#d67732',
               'CLE' : '#c9424a',
               'MIN' : '#a9333c',
               'DET' : '#001640',
               'CWS' : '#000000',
               'KC' : '#8b8143',
               'HOU' : '#fe6301',
               'OAK' : '#ecb233',
               'SEA' : '#195b4c',
               'LAA' : '#620000',
               'TEX' : '#aa343c',
            }
        )
        st.write(fig1)
       
    elif option == 'WAR & WHIP':
        df = pd.read_csv('data/Pstats_2022.csv')
        df2022 = pd.DataFrame(data = df,columns = df.columns)
        fig2 = px.scatter(
            df2022,
            x = 'WAR',
            y = 'WHIP',
            text = 'PLAYER',
            color = 'TEAM',
            size_max=30,
            height=500,
            width=800,
            size = 'W',
            color_discrete_map={
               'BOS' : '#c03832',
               'NYY' : '#cb483e',
               'TB' : '#01013b',
               'TOR' : '#436599',
                'BOL' : '#d67732',
               'CLE' : '#c9424a',
               'MIN' : '#a9333c',
               'DET' : '#001640',
               'CWS' : '#000000',
               'KC' : '#8b8143',
               'HOU' : '#fe6301',
               'OAK' : '#ecb233',
               'SEA' : '#195b4c',
               'LAA' : '#620000',
               'TEX' : '#aa343c',
            }
        )
        st.write(fig2)
    elif option == 'WAR & AVG':
        df = pd.read_csv('data/Pstats_2022.csv')
        df2022 = pd.DataFrame(data = df,columns = df.columns)
        fig3 = px.scatter(
            df2022,
            x = 'WAR',
            y = 'AVG',
            text = 'PLAYER',
            color = 'TEAM',
            size_max=30,
            height=500,
            width=800,
            size = 'W',
            color_discrete_map={
                'BOS' : '#c03832',
                'NYY' : '#cb483e',
                'TB' : '#01013b',
                'TOR' : '#436599',
                'BOL' : '#d67732',
                'CLE' : '#c9424a',
                'MIN' : '#a9333c',
                'DET' : '#001640',
                'CWS' : '#000000',
                'KC' : '#8b8143',
                'HOU' : '#fe6301',
                'OAK' : '#ecb233',
                'SEA' : '#195b4c',
                'LAA' : '#620000',
                'TEX' : '#aa343c',
            }
        )
        st.write(fig3)
    
    st.write("WAR&IPから見ると、IPが185、WARが3のあたりで線を引いて区切り4区分にまとめることができる。右下の区分はIPが少なくWARを多く稼ぐ、いわゆる「1イニングに対してのWARの数値が大きいプレイヤー」であり、ここではOtaniとVarlanderの双璧といった印象を受けた。")
    st.write('WAR&WHIP, WAR&AVGにおいては4選手ともリーグの中でも屈指の投球力を示しており、今季において4選手は他投手と比べて飛び抜けていたことが読み取れる。')
    st.write('')
    st.write('これらの情報を整理すると、')
    st.write("""
    - WARの度数分布は比較的左右対称であり、 **_2〜3_** に多く集まる傾向にある。
    - CYAを得るためには平均で **_6.8_** ほどWARを獲得する必要獲得する必要がある。ただし2016のようにPorcelloが貯金18などWAR以外に突出した成績を出した時、WAR以外での判断が強くなる可能性がある。
    - 大きなWARの数値を出すためには **_WHIPやAVG_** といった打者を出塁させない能力が大きな影響を与えている。
    """)

    st.write('といった点が挙げられ、今年に関してはWARは3選手の中でそれほど大きな差が出ず、かつVarlanderがWHIP、AVGの2部門でリーグトップの成績を挙げたため選出されたと考えられる。')
            




