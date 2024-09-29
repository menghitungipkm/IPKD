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

    # File upload for percentage data
    uploaded_percentage_file = st.file_uploader("Upload File Persentase (CSV)", type=["csv"])
    if uploaded_percentage_file is not None:
        df_percentage = pd.read_csv(uploaded_percentage_file)
    else:
        df_percentage = pd.read_csv('source/datasetreal.csv')  # Default file

    # Extract unique provinces and cities/districts
    unique_provinces = df_ipkd['Provinsi'].str.upper().unique()
    unique_cities = df_ipkd['Kota/Kabupaten'].str.upper().unique()

    # PEMILIHAN #
    provinsi = st.selectbox('Pilih Provinsi', unique_provinces, key='provinsi_selectbox')
    
    # Filter cities based on the selected province
    filtered_cities = df_ipkd[df_ipkd['Provinsi'].str.upper() == provinsi]['Kota/Kabupaten'].str.upper().unique()
    kota = st.selectbox('Pilih Kota/Kabupaten', filtered_cities, key='kota_selectbox')

    kolom_list = ['Kesehatan Balita', 'Kesehatan Reproduksi', 'Pelayanan Kesehatan', 
                  'Penyakit Tidak Menular', 'Penyakit Menular', 'Sanitasi dan Keadaan Lingkungan Hidup']

    field = st.selectbox('Pilih Kolom', kolom_list, key='field_selectbox')

    st.subheader(f'Nilai IPKD Provinsi {provinsi} di {kota}')

    st.subheader(f'kolom {field}')

    # MENAMPILKAN PLOT #
    # Ensure that comparisons are made correctly
    if 'Kota' in kota:
        data = df_ipkd[df_ipkd['Kota/Kabupaten'].str.upper() == kota.upper()]
    else:
        data = df_ipkd[df_ipkd['Kota/Kabupaten'].str.upper() == kota.upper()]

    tahun = data['Tahun'].astype(str).str[:4].tolist()
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
    tampilan_data = data[['Provinsi', 'Kota/Kabupaten', field, 'Tahun']]
    st.write(tampilan_data)

    # Langkah 1: Pilih Provinsi for percentage data
    unique_provinces_percentage = df_percentage['PROVINSI'].str.upper().unique()
    provinsi_percentage = st.selectbox("Pilih Provinsi untuk Persentase", unique_provinces_percentage)

    # Langkah 2: Pilih Kabupaten/Kota berdasarkan Provinsi
    filtered_kabupaten = df_percentage[df_percentage['PROVINSI'].str.upper() == provinsi_percentage]['KOTA/KABUPATEN'].str.upper().unique()
    kabupaten = st.selectbox("Pilih Kabupaten/Kota", filtered_kabupaten)

    # Langkah 3: Pilih opsi untuk grafik
    # You can automate the options for the graph based on the columns in the DataFrame
    options_for_graph = df_percentage.columns.tolist()
    options_for_graph.remove('PROVINSI')  # Exclude the province column
    options_for_graph.remove('KOTA/KABUPATEN')  # Exclude the city/district column
    options_for_graph.remove('TAHUN')  # Exclude the year column
    pilihan_grafik = st.selectbox("Pilih Data untuk Ditampilkan", options_for_graph)

    # Filter data berdasarkan pilihan pengguna
    if 'PROVINSI' in df_percentage.columns and 'KOTA/KABUPATEN' in df_percentage.columns:
        df_filtered = df_percentage[(df_percentage['PROVINSI'] == provinsi_percentage) & (df_percentage['KOTA/KABUPATEN'] == kabupaten)]

        # Langkah 4: Tampilkan grafik berdasarkan pilihan
        if not df_filtered.empty:
            st.write(f"Menampilkan grafik {pilihan_grafik} untuk {kabupaten}, {provinsi_percentage}")
            
            # Plot data dengan Plotly
            fig = px.line(df_filtered, x='TAHUN', y=pilihan_grafik, markers=True)
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
                yaxis=dict(tickfont=dict(color='black'))  # Set interval skala y-axis to 1
            )
            st.plotly_chart(fig)
        else:
            st.write("Data tidak ditemukan untuk pilihan yang dipilih.")
if __name__ == "__main__":
    app()
