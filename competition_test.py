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

st.title('test.csv ファイルに対する評価!')

# streamlitでファイルをアップロード
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
# アップロードしたファイルを読み込み
if uploaded_file is not None:
    input_df = pd.read_csv(uploaded_file, dtype=int, header=None)

    score_acc = round(accuracy_score(bank_test[colunm_name], input_df[0])*100, 4)
    score_rec = round(recall_score(bank_test[colunm_name], input_df[0])*100, 4)
    score_pre = round(precision_score(bank_test[colunm_name], input_df[0])*100, 4)
    score_f1 = round(f1_score(bank_test[colunm_name], input_df[0])*100, 4)
    score_auc = round(roc_auc_score(bank_test[colunm_name], input_df[0])*100, 4)

    # st.write('Accuracy：', score_acc, '%')
    # st.write('Recall：', score_rec, '%')
    # st.write('Precision：', score_pre, '%')
    # st.write('F1score：', score_f1, '%')
    # st.write('AUC：', score_auc, '%')
    # 表示オプションを変更

    df_score = pd.DataFrame({'Accuracy': [score_acc],
                            'Recall': [score_rec],
                            'Precision': [score_pre],
                            'F1score': [score_f1],
                            'AUC': [score_auc]}).T

    st.write(df_score)
    # print(df_score)