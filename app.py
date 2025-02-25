import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title='Data Sweeper', layout='wide', page_icon=':chart_with_upwards_trend:')
st.title('Data Sweeper')

st.write('Transform your files between CSV and Excel formats with built-in data cleaning and visualization!')

uploaded_files = st.file_uploader('Upload your files (CSV and Excel):', type=['csv', 'xlsx'], accept_multiple_files=True)

files_processed = False  

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == '.csv':
            df = pd.read_csv(file)
        elif file_ext == '.xlsx':
            df = pd.read_excel(file)
        else:
            st.error(f'Unsupported file type: {file_ext}')
            continue  

        st.write(f'**File name:** {file.name}')
        st.write(f'**File Size:** {file.size / 1024:.2f} KB')

        st.write('Preview of the DataFrame:')
        st.dataframe(df.head())

        st.subheader('Data Cleaning Options')
        cleaned = False 

        if st.checkbox(f'Clean data for {file.name}'):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f'Remove Duplicates from {file.name}'):
                    df.drop_duplicates(inplace=True)
                    st.write('Duplicates removed!')
                    cleaned = True  # ✅ Data clean ho gaya

            with col2:
                if st.button(f'Fill missing values for {file.name}'):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write('Missing values have been filled!')
                    cleaned = True  # ✅ Data clean ho gaya

        st.subheader('Select Columns to Convert')
        columns = st.multiselect(f'Choose columns for {file.name}', df.columns, default=df.columns)
        df = df[columns]

        st.subheader('Data Visualization')
        if st.checkbox(f'Show Visualization for {file.name}'):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        st.subheader('Conversion Options')
        conversion_type = st.radio(f'Convert {file.name} to:', ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = 'text/csv'
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            buffer.seek(0)

            st.download_button(
                label=f'Download {file_name} as {conversion_type}',
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )
            files_processed = True  


if files_processed:
    st.success('All files processed successfully! 🎉')
