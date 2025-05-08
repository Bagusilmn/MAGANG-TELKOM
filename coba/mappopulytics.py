import streamlit as st
import geopandas as gpd
import folium
import pandas as pd
from streamlit_folium import st_folium
import branca.colormap as cm
from shapely.geometry import Point

# Load shapefile
shapefile_path = r"D:\Magang telkom\coba\[LapakGIS.com] KAB. JEMBER\ADMINISTRASIDESA_AR_25K.shp"
gdf = gpd.read_file(shapefile_path)
gdf = gdf.dissolve(by=["WADMKC", "NAMOBJ"], as_index=False)

# Load data CSV penduduk
csv_path = "D:/Magang telkom/coba/Dataset_PetaKabJember - Sheet1.csv"
df_penduduk = pd.read_csv(csv_path)

# Hitung luas dalam km²
gdf_utm = gdf.to_crs(epsg=32748)
gdf_utm["area_m2"] = gdf_utm.geometry.area
gdf_utm["area_km2"] = gdf_utm["area_m2"] / 1_000_000
gdf["area_km2"] = gdf_utm["area_km2"]


# Bersihkan dan ubah kolom jumlah penduduk ke numerik
df_penduduk["Jumlah Penduduk"] = df_penduduk["Jumlah Penduduk"].astype(str).str.replace(".", "").str.replace(",", "")
df_penduduk["Jumlah Penduduk"] = pd.to_numeric(df_penduduk["Jumlah Penduduk"], errors='coerce')
df_penduduk.rename(columns={"Kecamatan": "WADMKC", "Kelurahan/Desa": "NAMOBJ"}, inplace=True) #merge
# Merge ke GeoDataFrame
gdf = gdf.merge(df_penduduk[["WADMKC", "NAMOBJ", "Jumlah Penduduk"]], on=["WADMKC", "NAMOBJ"], how="left")
st.write("Jumlah wilayah berhasil dapat data penduduk:", gdf['Jumlah Penduduk'].notna().sum())


# Hitung kepadatan penduduk (orang per km2)
gdf['Kepadatan'] = gdf['Jumlah Penduduk'] / gdf['area_km2'].round(2)
gdf['Kepadatan'] = gdf['Kepadatan'].fillna(0)

# Clamp nilai kepadatan
gdf['Kepadatan Clamped'] = gdf['Kepadatan'].clip(upper=2500)  # maks 30.000 orang/km2
valid_kepadatan = gdf['Kepadatan Clamped'].dropna()
min_density = valid_kepadatan.min()
max_density = valid_kepadatan.max()

density_colormap = cm.linear.RdYlGn_11.scale(min_density, max_density)
density_colormap = cm.LinearColormap(
    colors=density_colormap.colors[::-1],
    index=density_colormap.index,
    vmin=min_density,
    vmax=max_density
)


# Sidebar filter
st.sidebar.title("Filter Wilayah")
kecamatan_list = sorted(gdf['WADMKC'].unique())
selected_kecamatan = st.sidebar.selectbox("Pilih Kecamatan", ["Semua"] + kecamatan_list)
if selected_kecamatan != "Semua":
    desa_list = sorted(gdf[gdf['WADMKC'] == selected_kecamatan]['NAMOBJ'].unique())
else:
    desa_list = sorted(gdf['NAMOBJ'].unique())

selected_desa = st.sidebar.selectbox("Pilih Desa", ["Semua"] + desa_list)

# Identifikasi wilayah yang dipilih
highlight_geom = None
if selected_kecamatan != "Semua" and selected_desa != "Semua":
    highlight_geom = gdf[(gdf['WADMKC'] == selected_kecamatan) & (gdf['NAMOBJ'] == selected_desa)]
elif selected_kecamatan != "Semua":
    highlight_geom = gdf[gdf['WADMKC'] == selected_kecamatan]
elif selected_desa != "Semua":
    highlight_geom = gdf[gdf['NAMOBJ'] == selected_desa]

# Center Map
if highlight_geom is not None and not highlight_geom.empty:
    centroid = highlight_geom.geometry.unary_union.centroid
    m = folium.Map(location=[centroid.y, centroid.x], zoom_start=13)
else:
    center = gdf.geometry.unary_union.centroid.coords[:][0]
    m = folium.Map(location=[center[1], center[0]], zoom_start=10)

# Styling berdasarkan kepadatan
def style_density(feature):
    kepadatan = feature['properties'].get('Kepadatan')
    if kepadatan is None or pd.isna(kepadatan):
        fill_color = '#D3D3D3'  # Abu-abu untuk yang tidak ada data
    else:
        fill_color = density_colormap(kepadatan)
    return {
        'fillColor': fill_color,
        'color': 'black',
        'weight': 1,
        'fillOpacity': 1,
    }

# Highlight style
def highlight_style(feature):
    return {
        'color': 'red',
        'weight': 3,
        'fillOpacity': 0.9,
    }

# Tampilkan semua wilayah
folium.GeoJson(
    gdf,
    name="Kepadatan Penduduk",
    style_function=style_density,
    highlight_function=highlight_style,
    tooltip=folium.GeoJsonTooltip(
        fields=["WADMKC", "NAMOBJ", "Jumlah Penduduk", "Kepadatan"],
        aliases=["Kecamatan:", "Desa:", "Jumlah Penduduk:", "Kepadatan Penduduk:"],
        sticky=True,
        opacity=0.9,
        direction='auto'
    ),
        popup=folium.GeoJsonPopup(
        fields=["WADMPR", "WADMKK", "WADMKC", "NAMOBJ", "area_km2", "Jumlah Penduduk", "Kepadatan"],
        aliases=["Provinsi:", "Kabupaten:", "Kecamatan:", "Desa:", "Luas Area:", "Jumlah Penduduk:", "Kepadatan Penduduk:"],
        labels=True
    ),
    zoom_on_click=False
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
            fields=["WADMPR", "WADMKK", "WADMKC", "NAMOBJ", "area_km2", "Kepadatan"],
            aliases=["Provinsi:", "Kabupaten:", "Kecamatan:", "Desa:", "Luas Area:", "Kepadatan Penduduk:"],
            sticky=False
        )
    ).add_to(m)

density_colormap.add_to(m)



# Tampilkan peta
st_data = st_folium(m, width=800, height=600)

