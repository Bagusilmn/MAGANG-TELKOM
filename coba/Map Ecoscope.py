import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from shapely.geometry import Point
import pandas as pd

# --- LOAD SHAPEFILE DAN DATA CSV ---

shapefile_path = r"D:\Magang telkom\coba\[LapakGIS.com] KAB. JEMBER\ADMINISTRASIDESA_AR_25K.shp"
gdf = gpd.read_file(shapefile_path)

gdf_utm = gdf.to_crs(epsg=32748)
gdf_utm["area_m2"] = gdf_utm.geometry.area
gdf_utm["area_km2"] = gdf_utm["area_m2"] / 1_000_000

# Load CSV tingkat ekonomi
ekonomi_df = pd.read_csv("D:\Magang telkom\coba\hasil_analisis_ekonomi.csv")

# Normalisasi kecamatan agar match
ekonomi_df['Kecamatan'] = ekonomi_df['Kecamatan'].str.strip().str.upper()
gdf['WADMKC'] = gdf['WADMKC'].str.strip().str.upper()

# Merge dengan GeoDataFrame
gdf = gdf.merge(ekonomi_df, how='left', left_on='WADMKC', right_on='Kecamatan')
gdf["area_km2"] = gdf_utm["area_km2"]

# Warna berdasarkan tingkat ekonomi
tingkat_warna = {
    'TINGGI': 'green',  # hijau 
    'SEDANG': 'yellow',  # kuning 
    'RENDAH': 'red'   # merah
}

# --- SIDEBAR FILTER ---
st.sidebar.title("Filter Wilayah")
kecamatan_list = sorted(gdf['WADMKC'].unique())
selected_kecamatan = st.sidebar.selectbox("Pilih Kecamatan", ["Semua"] + kecamatan_list)

if selected_kecamatan != "Semua":
    desa_list = sorted(gdf[gdf['WADMKC'] == selected_kecamatan]['NAMOBJ'].unique())
else:
    desa_list = sorted(gdf['NAMOBJ'].unique())

selected_desa = st.sidebar.selectbox("Pilih Desa", ["Semua"] + desa_list)

# --- IDENTIFIKASI WILAYAH DIPILIH ---
highlight_geom = None

if selected_kecamatan != "Semua" and selected_desa != "Semua":
    highlight_geom = gdf[(gdf['WADMKC'] == selected_kecamatan) & (gdf['NAMOBJ'] == selected_desa)]
elif selected_kecamatan != "Semua":
    highlight_geom = gdf[gdf['WADMKC'] == selected_kecamatan]
elif selected_desa != "Semua":
    highlight_geom = gdf[gdf['NAMOBJ'] == selected_desa]

# --- BUAT PETA ---
if highlight_geom is not None and not highlight_geom.empty:
    centroid = highlight_geom.geometry.unary_union.centroid
    m = folium.Map(location=[centroid.y, centroid.x], zoom_start=13)
else:
    center = gdf.geometry.unary_union.centroid.coords[:][0]
    m = folium.Map(location=[center[1], center[0]], zoom_start=10)

# Fungsi pewarnaan berdasarkan tingkat ekonomi
def style_by_ekonomi(feature):
    tingkat = feature['properties'].get('Tingkat_Ekonomi', None)
    if isinstance(tingkat, str):
        tingkat = tingkat.upper()
    else:
        tingkat = None
    warna = tingkat_warna.get(tingkat, 'grey')  # Abu-abu jika tidak ada data
    return {
        'fillColor': warna,
        'color': 'white',
        'weight': 2,
        'fillOpacity': 1,
    }

# Tambahkan layer GeoJson utama
folium.GeoJson(
    gdf,
    name="Tingkat Ekonomi",
    style_function=style_by_ekonomi,
    highlight_function=lambda feature: {
        # 'fillColor': '#ffff00',
        'color': 'red',
        'weight': 3,
        # 'fillOpacity': 0.9,
    },
    tooltip=folium.GeoJsonTooltip(
        fields=["WADMKC", "NAMOBJ", "Tingkat_Ekonomi"],
        aliases=["Kecamatan:", "Desa:", "Tingkat Ekonomi:"],
        sticky=True,
        opacity=0.9,
        direction='auto'
    ),
    popup=folium.GeoJsonPopup(
        fields=["WADMPR", "WADMKK", "WADMKC", "NAMOBJ", "area_km2", "Tingkat_Ekonomi"],
        aliases=["Provinsi:", "Kabupaten:", "Kecamatan:", "Desa:", "Luas Area:", "Tingkat Ekonomi:"],
        labels=True
    ),
    zoom_on_click=True
).add_to(m)

# Tambahkan highlight jika wilayah dipilih
if highlight_geom is not None and not highlight_geom.empty:
    folium.GeoJson(
        highlight_geom,
        name="Wilayah Dipilih",
        style_function=lambda feature: {
            'fillColor': 'none',
            'color': 'blue',
            'weight': 4,
            'fillOpacity': 0,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["WADMPR", "WADMKK", "WADMKC", "NAMOBJ", "area_km2", "Tingkat_Ekonomi"],
            aliases=["Provinsi:", "Kabupaten:", "Kecamatan:", "Desa:", "Luas Area:", "Tingkat Ekonomi:"],
            sticky=False
        )
    ).add_to(m)

# Tampilkan peta
st_data = st_folium(m, width=800, height=600)

clicked_location = st_data.get("last_clicked")
if clicked_location:
    point = Point(clicked_location["lng"], clicked_location["lat"])
    matched_area = gdf[gdf.geometry.contains(point)]

    if not matched_area.empty:
        filter_result = matched_area
    else:
        filter_result = highlight_geom if highlight_geom is not None and not highlight_geom.empty else gdf
