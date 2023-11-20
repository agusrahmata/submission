import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# load data
main_data_df = pd.read_csv("main_data.csv")

# mengganti judul kolom dteday menjadi dateday
# mengganti judul kolom yr menjadi year
# mengganti judul kolom hr menjadi hour
# mengganti judul kolom weekday menjadi wkday
# mengganti judul kolom cnt menjadi total_user
main_data_df.columns = ["instant", "dateday", "season", "year", "mnth", "hour", "holiday", "wkday", "workingday", "weathersit", "temp", "atemp", "hum", "windspeed", "casual", "registered", "total_user"]

# mengganti tipe data pada kolom dteday menjadi datetime
datetime_columns = ["dateday"]
for column in datetime_columns:
  main_data_df[column] = pd.to_datetime(main_data_df[column])

# membuat kolom baru month yang berisikan nama-nama bulan yang merupakan perubahan dari kolom mnth
import calendar
def angka_ke_bulan(angka):
    return calendar.month_name[angka]
main_data_df['month'] = main_data_df['mnth'].apply(angka_ke_bulan)
# membuat kolom month jadi berurutan dari Januari sampai Desember
main_data_df["month"] = pd.Categorical(main_data_df["month"], categories=[
    "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"
], ordered=True)

# membuat kolom baru weekday yang berisikan nama-nama hari yang merupakan perubahan dari kolom wkday
main_data_df["weekday"] = main_data_df["wkday"].replace({0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday"})
# membuat kolom weekday jadi berurutan dari Minggu sampai Sabtu
main_data_df["weekday"] = pd.Categorical(main_data_df["weekday"], categories=[
    "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"
], ordered=True)

# helper function yang dibutuhkan untuk menyiapkan berbagai dataframe
def create_bybulan_df(df):
    bybulan_df = main_data_df.groupby(by=["month"]).agg({
    "casual": "sum",
    "registered": "sum"
    }).reset_index()

    return bybulan_df

def create_byhari_df(df):
    byhari_df = main_data_df.groupby(by=["weekday"]).agg({
    "casual": "sum",
    "registered": "sum"
    }).reset_index()

    return byhari_df

def create_byjam_df(df):
    byjam_df = main_data_df.groupby(by=["hour"]).agg({
    "casual": "sum",
    "registered": "sum"
    }).reset_index()

    return byjam_df

# memanggil helper function yang telah dibuat
byhari_df = create_byhari_df(main_data_df)
byjam_df = create_byjam_df(main_data_df)
bybulan_df = create_bybulan_df(main_data_df)

# membuat dashboard dengan bentuk tab
st.title('Bike Sharing Dashboard')
tab1, tab2, tab3 = st.tabs(["Penggunaan per Jam", "Penggunaan per Hari", "Penggunaan per Bulan"])

# membuat tab untuk penggunaan per jam
with tab1:
    st.header("Penggunaan per Jam")
    
    fig, ax = plt.subplots()
    sns.set(style='whitegrid')
    sns.barplot(x="hour", y='value', hue='variable', data=pd.melt(byjam_df, ["hour"]))
    ax.set_ylabel("Jumlah Pengguna")
    ax.set_xlabel("Jam")
    st.pyplot(fig)
    
    with st.expander("Keterangan"):
        st.write(
            """Untuk casual user, penggunaan terbanyak adalah pada jam siang sampai sore, yaitu jam 13 sampai 17.
            Sedangkan penggunaan terbanyak untuk registered user adalah pada pagi jam 8 dan sore jam 17 dan jam 18.
            Kesimpulannya adalah penggunaan registered user dipergunakan
            untuk keperluan aktivitas berangkat kerja/sekolah dan pulang kerja/sekolah.
            """
        )

# membuat tab untuk penggunaan per hari
with tab2:
    st.header("Penggunaan per Hari")

    fig, ax = plt.subplots()
    sns.set(style='whitegrid')
    sns.barplot(x='weekday', y='value', hue='variable', data=pd.melt(byhari_df, ['weekday']))
    ax.set_ylabel("Jumlah Pengguna")
    ax.set_xlabel("Hari")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

    with st.expander("Keterangan"):
        st.write(
            """Penggunaan terbanyak untuk casual user adalah akhir pekan, Sabtu dan Minggu.
            Sedangkan untuk registered user, penggunaan terbanyak adalah pada hari Kamis.
            """
        )

# membuat tab untuk penggunaan per jam
with tab3:
    st.header("Penggunaan per Bulan")

    fig, ax = plt.subplots()
    sns.set(style='whitegrid')
    sns.barplot(x='month', y='value', hue='variable', data=pd.melt(bybulan_df, ['month']))
    ax.set_ylabel("Jumlah Pengguna")
    ax.set_xlabel("Bulan")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

    with st.expander("Keterangan"):
        st.write(
            """Terdapat adanya pola dimana periode Desember-Januari-Februari (musim dingin),
            terjadi penurunan jumlah user. Lalu jumlah mulai naik lagi ketika memasuki Maret-April-Juni (musim semi).
            Kemudian terjadi puncak user terbanyak adalah periode Juli-Agustus-September (musim panas).
            """
        )

# membuat watermark
st.caption('Copyright © agusrahmata 2023')