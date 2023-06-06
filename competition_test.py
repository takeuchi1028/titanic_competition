import streamlit as st
import pandas as pd

from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
# AUC
from sklearn.metrics import roc_auc_score

# Load the data
bank_test = pd.read_csv('submission_answer.csv')
# 目的変数の変数名
colunm_name = 'Survived'
# result 列のfailを0、successを1に変換
# bank_test[colunm_name] = bank_test[colunm_name].map({'fail': 0, 'success': 1})

st.title('Leaderboard for test.csv')
ranking_df = pd.read_csv('ranking.csv')

st.sidebar.title('評価指標')
option = ['F1-score', 'Accuracy', 'Recall', 'Precision', 'AUC']
selected_score = st.sidebar.selectbox('Select your option', option)


# streamlitでテキストを入力
name = st.text_input('ニックネームを入力してください。')
group_name = st.text_input('グループ名を入力してください。')

# streamlitでファイルをアップロード
uploaded_file = st.file_uploader("CSV ファイルをアップロードしてください。", type="csv")

# アップロードしたファイルを読み込み
if st.button('評価') and uploaded_file is not None:

    input_df = pd.read_csv(uploaded_file)

    score_acc = round(accuracy_score(bank_test[colunm_name], input_df[colunm_name])*100, 4)
    score_rec = round(recall_score(bank_test[colunm_name], input_df[colunm_name])*100, 4)
    score_pre = round(precision_score(bank_test[colunm_name], input_df[colunm_name])*100, 4)
    score_f1 = round(f1_score(bank_test[colunm_name], input_df[colunm_name])*100, 4)
    score_auc = round(roc_auc_score(bank_test[colunm_name], input_df[colunm_name])*100, 4)

    # st.write('Accuracy：', score_acc, '%')
    # st.write('Recall：', score_rec, '%')
    # st.write('Precision：', score_pre, '%')
    # st.write('F1score：', score_f1, '%')
    # st.write('AUC：', score_auc, '%')
    # 表示オプションを変更

    df_score = pd.DataFrame({'Name': [name],
                            'Group': [group_name],
                            'Accuracy': [score_acc],
                            'Recall': [score_rec],
                            'Precision': [score_pre],
                            'F1-score': [score_f1],
                            'AUC': [score_auc]})
    
    # ranking_df に df_score と同じ行があれば
    if ranking_df[ranking_df['Name'] == name].empty:
        ranking_df = pd.concat([ranking_df, df_score], axis=0)
    
    ranking_df.to_csv('ranking.csv', index=False)
    # print(df_score)

st.sidebar.download_button('csvファイルを出力', ranking_df.to_csv(index=False), 'ranking.csv')
cleared_num = st.sidebar.number_input('消去するインデックスを入力', min_value=0)
if st.sidebar.button('消去'):
    ranking_df = ranking_df.drop(index=cleared_num)
    ranking_df.to_csv('ranking.csv', index=False)

ranking_df = ranking_df.sort_values(selected_score, ascending=False)
rank = ranking_df[selected_score].rank(method='min', ascending=False).astype(int)
ranking_df.insert(0, 'Rank', rank)
ranking_df = ranking_df.sort_values('Rank', ascending=True)
ranking_df = ranking_df.reset_index(drop=True)

st.table(ranking_df)

# # DataFrameをHTMLに変換し、インデックスを非表示にする
# df_html = ranking_df.to_html(index=False)

# # HTMLを表示
# st.write(df_html, unsafe_allow_html=True)