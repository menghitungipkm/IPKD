import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import os

def app():
    # Fungsi untuk memuat model
    @st.cache_resource
    def load_model():
        try:
            return joblib.load('voting_classifier_model.pkl')
        except Exception as e:
            st.error(f"Error loading the model: {e}")
            return None

    # Fungsi untuk memuat data
    @st.cache_data
    def load_data(file):
        data = pd.read_excel(file)
        data['Tahun'] = data['Tahun'].astype(str)
        # Normalize column names: lowercase, remove leading/trailing spaces, replace internal multiple spaces with a single space
        data.columns = [col.strip().lower().replace(' ', '_') for col in data.columns]
        return data

    # Set page title
    st.title("Visualisasi Gabungan Data")

    # File upload section
    uploaded_file = st.file_uploader("Silahkan Upload file Excel", type=['xlsx'])
    if uploaded_file is not None:
        data = load_data(uploaded_file)
    else:
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "source/kota_kabupaten.xlsx")
        data = load_data(file_path)

    # Sidebar untuk memilih region
    if 'provinsi' not in data.columns:
        st.error("Kolom 'provinsi' tidak ditemukan!")
        return  # Keluar jika kolom tidak ditemukan

    regions = data['provinsi'].unique()
    region = st.selectbox("Pilih Wilayah", regions)

    # Filter data berdasarkan wilayah
    region_data = data[data['provinsi'] == region]

    # Tambahkan beberapa perhitungan yang bisa dibuat grafiknya
    # 1. Kepadatan Penduduk (Penduduk per km2)
    if 'jumlah_penduduk_l_+_p' in region_data.columns and 'luas_wilayah_(km2)' in region_data.columns:
        region_data['kepadatan_penduduk'] = region_data['jumlah_penduduk_l_+_p'] / region_data['luas_wilayah_(km2)']

    # 2. Rasio Rumah Tangga per Desa
    if 'jumlah_rumah_tangga' in region_data.columns and 'desa' in region_data.columns:
        region_data['rasio_rumah_tangga_per_desa'] = region_data['jumlah_rumah_tangga'] / region_data['desa']

    # 3. Rasio Rumah Tangga per Kelurahan
    if 'jumlah_rumah_tangga' in region_data.columns and 'kelurahan' in region_data.columns:
        region_data['rasio_rumah_tangga_per_kelurahan'] = region_data['jumlah_rumah_tangga'] / region_data['kelurahan']

    # 4. Total Wilayah per Desa dan Kelurahan
    if 'luas_wilayah_(km2)' in region_data.columns and 'desa_+_kelurahan' in region_data.columns:
        region_data['luas_wilayah_per_desa_kelurahan'] = region_data['luas_wilayah_(km2)'] / region_data['desa_+_kelurahan']

    # Fungsi untuk memperbarui layout pada grafik
    def customize_layout(fig):
        fig.update_layout(
            title=dict(font=dict(color='black', size=20)),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='black'),
            xaxis_title=dict(font=dict(color='black')),
            yaxis_title=dict(font=dict(color='black')),
            xaxis=dict(tickfont=dict(color='black')),
            yaxis=dict(tickfont=dict(color='black')),
            legend=dict(
                title=dict(text='Kota/Kabupaten', font=dict(color='black')),
                font=dict(color='black')
            )
        )
        return fig

    # Visualisasi berbagai grafik gabungan dalam satu kolom (8 grafik berturut-turut)
    st.header(f"Visualisasi Data untuk {region}")

    # 1. Grafik Kepadatan Penduduk
    if 'kepadatan_penduduk' in region_data.columns:
        st.subheader(f"Kepadatan Penduduk di {region}")
        fig_density = px.line(region_data, x='tahun', y='kepadatan_penduduk', color='kota/kabupaten',
                              title=f"Kepadatan Penduduk di {region} per Tahun")
        st.plotly_chart(customize_layout(fig_density))

    # 2. Grafik Rasio Rumah Tangga per Desa
    if 'rasio_rumah_tangga_per_desa' in region_data.columns:
        st.subheader(f"Rasio Rumah Tangga per Desa di {region}")
        fig_ratio_desa = px.bar(region_data, x='tahun', y='rasio_rumah_tangga_per_desa', color='kota/kabupaten',
                                title=f"Rasio Rumah Tangga per Desa di {region}")
        st.plotly_chart(customize_layout(fig_ratio_desa))

    # 3. Grafik Luas Wilayah per Desa dan Kelurahan
    if 'luas_wilayah_per_desa_kelurahan' in region_data.columns:
        st.subheader(f"Luas Wilayah per Desa/Kelurahan di {region}")
        fig_area_village = px.scatter(region_data, x='tahun', y='luas_wilayah_per_desa_kelurahan', color='kota/kabupaten',
                                      size='luas_wilayah_per_desa_kelurahan',
                                      title=f"Luas Wilayah per Desa/Kelurahan di {region}")
        st.plotly_chart(customize_layout(fig_area_village))

    # 4. Grafik Rasio Rumah Tangga per Kelurahan
    if 'rasio_rumah_tangga_per_kelurahan' in region_data.columns:
        st.subheader(f"Rasio Rumah Tangga per Kelurahan di {region}")
        fig_ratio_kelurahan = px.line(region_data, x='tahun', y='rasio_rumah_tangga_per_kelurahan', color='kota/kabupaten',
                                      title=f"Rasio Rumah Tangga per Kelurahan di {region}")
        st.plotly_chart(customize_layout(fig_ratio_kelurahan))

    # 5. Grafik Jumlah Penduduk
    if 'jumlah_penduduk_l_+_p' in region_data.columns:
        st.subheader(f"Jumlah Penduduk di {region}")
        fig_population = px.line(region_data, x='tahun', y='jumlah_penduduk_l_+_p', color='kota/kabupaten',
                                 title=f"Total Penduduk di {region} per Tahun")
        st.plotly_chart(customize_layout(fig_population))

    # 6. Grafik Jumlah Rumah Tangga
    if 'jumlah_rumah_tangga' in region_data.columns:
        st.subheader(f"Jumlah Rumah Tangga di {region}")
        fig_households = px.line(region_data, x='tahun', y='jumlah_rumah_tangga', color='kota/kabupaten',
                                 title=f"Total Rumah Tangga di {region} per Tahun")
        st.plotly_chart(customize_layout(fig_households))

    # 7. Grafik Total Desa + Kelurahan
    if 'desa_+_kelurahan' in region_data.columns:
        st.subheader(f"Total Desa + Kelurahan di {region}")
        fig_villages = px.bar(region_data, x='kota/kabupaten', y='desa_+_kelurahan', color='kota/kabupaten',
                              title=f"Total Desa + Kelurahan per Kota/Kabupaten di {region}")
        st.plotly_chart(customize_layout(fig_villages))

    # 8. Grafik Pertumbuhan Persentase Jumlah Penduduk
    if 'jumlah_penduduk_l_+_p' in region_data.columns:
        st.subheader(f"Pertumbuhan Persentase Jumlah Penduduk di {region}")
        region_data['growth_population'] = region_data.groupby('kota/kabupaten')['jumlah_penduduk_l_+_p'].pct_change() * 100
        fig_growth = px.line(region_data, x='tahun', y='growth_population', color='kota/kabupaten',
                             title=f"Pertumbuhan Persentase Jumlah Penduduk di {region} per Tahun")
        st.plotly_chart(customize_layout(fig_growth))

if __name__ == "__main__":
    app()
