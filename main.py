import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.title('데이터 분석 웹앱')

# 1. CSV 파일 업로드
uploaded_file = st.file_uploader('CSV 파일을 업로드하세요', type=['csv'])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader('원본 데이터 미리보기')
    st.dataframe(df.head())

    # 2. 데이터 전처리
    st.subheader('결측치 처리')
    missing_cols = df.columns[df.isnull().any()].tolist()
    if missing_cols:
        st.write(f"결측치가 있는 컬럼: {missing_cols}")
        method = st.selectbox('결측치 처리 방법을 선택하세요', ['제거', '평균값 대체', '최빈값 대체'])
        if st.button('결측치 처리 실행'):
            if method == '제거':
                df = df.dropna()
            elif method == '평균값 대체':
                df = df.fillna(df.mean(numeric_only=True))
            elif method == '최빈값 대체':
                for col in missing_cols:
                    df[col] = df[col].fillna(df[col].mode()[0])
            st.success('결측치 처리가 완료되었습니다.')
            st.dataframe(df.head())
    else:
        st.write('결측치가 없습니다.')

    # 3. 기본 통계
    st.subheader('기본 통계')
    st.dataframe(df.describe())

    # 4. 시각화
    st.subheader('데이터 시각화')
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    if numeric_cols:
        plot_type = st.selectbox('시각화 종류를 선택하세요', ['히스토그램', '상관관계 히트맵'])
        if plot_type == '히스토그램':
            col = st.selectbox('컬럼 선택', numeric_cols)
            fig, ax = plt.subplots()
            df[col].hist(ax=ax, bins=30)
            ax.set_title(f'{col} 히스토그램')
            st.pyplot(fig)
        elif plot_type == '상관관계 히트맵':
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm', ax=ax)
            st.pyplot(fig)
    else:
        st.write('수치형 컬럼이 없습니다.')
else:
    st.info('CSV 파일을 먼저 업로드하세요.')
