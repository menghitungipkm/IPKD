import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def app():
    st.title('Grafik IPKD')  

    # File upload for IPKD data
    uploaded_ipkd_file = st.file_uploader("Upload File IPKD (Excel)", type=["xlsx"])
    if uploaded_ipkd_file is not None:
        df_ipkd = pd.read_excel(uploaded_ipkd_file, sheet_name='Hasil_Akhir')
    else:
        df_ipkd = pd.read_excel('source/ipkd_results.xlsx')  # Default file

    # Convert column names to lowercase
    df_ipkd.columns = df_ipkd.columns.str.lower()

    # File upload for percentage data
    uploaded_percentage_file = st.file_uploader("Upload File Persentase (CSV)", type=["csv"])
    if uploaded_percentage_file is not None:
        df_percentage = pd.read_csv(uploaded_percentage_file)
    else:
        df_percentage = pd.read_csv('source/datasetreal.csv')  # Default file

    # Convert column names to lowercase
    df_percentage.columns = df_percentage.columns.str.lower()

    # Extract unique provinces and cities/districts
    unique_provinces = df_ipkd['provinsi'].str.upper().unique()
    unique_cities = df_ipkd['kota/kabupaten'].str.upper().unique()

    # PEMILIHAN #
    provinsi = st.selectbox('Pilih Provinsi', unique_provinces, key='provinsi_selectbox')
    
    # Filter cities based on the selected province
    filtered_cities = df_ipkd[df_ipkd['provinsi'].str.upper() == provinsi]['kota/kabupaten'].str.upper().unique()
    kota = st.selectbox('Pilih Kota/Kabupaten', filtered_cities, key='kota_selectbox')

    kolom_list = ['kesehatan balita', 'kesehatan reproduksi', 'pelayanan kesehatan', 
                  'penyakit tidak menular', 'penyakit menular', 'sanitasi dan keadaan lingkungan hidup']

    field = st.selectbox('Pilih Kolom', kolom_list, key='field_selectbox')

    st.subheader(f'Nilai IPKD Provinsi {provinsi} di {kota}')
    st.subheader(f'kolom {field}')

    # MENAMPILKAN PLOT #
    # Ensure that comparisons are made correctly
    data = df_ipkd[df_ipkd['kota/kabupaten'].str.upper() == kota.upper()]
    
    tahun = data['tahun'].astype(str).str[:4].tolist()
    value = data[field].tolist()

    # Using Plotly to create an interactive graph
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=tahun, y=value, mode='lines+markers', name=field, line=dict(color='red', width=2)))
    
    fig.update_layout(
        title=dict(text=f"Grafik {field} di {kota} ({provinsi})", font=dict(color='black', size=20)),
        xaxis_title=dict(text='Tahun', font=dict(color='black', size=14, family="Arial", weight="bold")),
        yaxis_title=dict(text='Nilai', font=dict(color='black', size=14, family="Arial", weight="bold")),
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='white',
        font=dict(color='black', weight="bold"),
        xaxis=dict(tickfont=dict(color='black')),
        yaxis=dict(tickfont=dict(color='black'))
    )

    st.plotly_chart(fig)

    # TAMPILAN TABEL
    st.subheader('Tabel')
    tampilan_data = data[['provinsi', 'kota/kabupaten', field, 'tahun']]
    st.write(tampilan_data)

    # Langkah 1: Pilih Provinsi for percentage data
    unique_provinces_percentage = df_percentage['provinsi'].str.upper().unique()
    provinsi_percentage = st.selectbox("Pilih Provinsi untuk Persentase", unique_provinces_percentage)

    # Langkah 2: Pilih Kabupaten/Kota berdasarkan Provinsi
    filtered_kabupaten = df_percentage[df_percentage['provinsi'].str.upper() == provinsi_percentage]['kota/kabupaten'].str.upper().unique()
    kabupaten = st.selectbox("Pilih Kabupaten/Kota", filtered_kabupaten)

    # Langkah 3: Pilih opsi untuk grafik
    options_for_graph = df_percentage.columns.tolist()
    options_for_graph.remove('provinsi')  # Exclude the province column
    options_for_graph.remove('kota/kabupaten')  # Exclude the city/district column
    options_for_graph.remove('tahun')  # Exclude the year column
    pilihan_grafik = st.selectbox("Pilih Data untuk Ditampilkan", options_for_graph)

    # Filter data berdasarkan pilihan pengguna
    if 'provinsi' in df_percentage.columns and 'kota/kabupaten' in df_percentage.columns:
        df_filtered = df_percentage[(df_percentage['provinsi'] == provinsi_percentage) & (df_percentage['kota/kabupaten'] == kabupaten)]

        # Langkah 4: Tampilkan grafik berdasarkan pilihan
        if not df_filtered.empty:
            st.write(f"Menampilkan grafik {pilihan_grafik} untuk {kabupaten}, {provinsi_percentage}")
            
            # Plot data dengan Plotly
            fig = px.line(df_filtered, x='tahun', y=pilihan_grafik, markers=True)
            fig.update_traces(line=dict(color='red', width=2))  
            fig.update_layout(
                title=dict(text=f"Grafik {pilihan_grafik} di {kabupaten} ({provinsi_percentage})", font=dict(color='black', size=20)),
                xaxis_title=dict(text='Tahun', font=dict(color='black', size=14, family="Arial", weight="bold")),
                yaxis_title=dict(text='Nilai (%)', font=dict(color='black', size=14, family="Arial", weight="bold")),
                template='plotly_dark',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='white',
                font=dict(color='black', weight="bold"),
                xaxis=dict(tickfont=dict(color='black')),
                yaxis=dict(tickfont=dict(color='black'))  
            )
            st.plotly_chart(fig)
        else:
            st.write("Data tidak ditemukan untuk pilihan yang dipilih.")

if __name__ == "__main__":
    app()
