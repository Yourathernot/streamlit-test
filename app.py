import pandas as pd
import requests
import streamlit as st

st.title('Тестовое задание по streamlit')
st.header("Заголовок")
st.subheader("Подзаголовок")
st.write("""текст""")
st.html("<p>HTML</p>")
st.markdown("""
**:rainbow[просто сказка]**
""")
st.image("https://media.tenor.com/46Weg3HrCfEAAAAi/horse-fat.gif")

if st.button("Ура!"):
    st.balloons()

url = "https://jsonplaceholder.typicode.com/users"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    df = pd.json_normalize(data)  # Flatten nested fields

    df = df.rename(columns={
        'id': 'User ID',
        'name': 'Full Name',
        'username': 'Username',
        'email': 'Email Address',
        'phone': 'Phone Number',
        'website': 'Website',
        'address.street': 'Street',
        'address.suite': 'Suite',
        'address.city': 'City',
        'address.zipcode': 'Zip Code',
        'address.geo.lat': 'Latitude',
        'address.geo.lng': 'Longitude',
        'company.name': 'Company Name',
        'company.catchPhrase': 'Catch Phrase',
        'company.bs': 'Business'
    })

    # Convert latitude and longitude to float
    df['Latitude'] = df['Latitude'].astype(float)
    df['Longitude'] = df['Longitude'].astype(float)

    city_list = sorted(df['City'].unique())
    selected_city = st.selectbox("Фильтр по городу", options=["Все"] + city_list)

    if selected_city != "Все":
        df = df[df['City'] == selected_city]

    df = df.set_index('User ID')

    st.subheader("Таблица пользователей")
    st.dataframe(df)
    if not df.empty:
        st.subheader("Расположение пользователей")
        map_df = df[['Latitude', 'Longitude']].copy()
        map_df = map_df.rename(columns={'Latitude': 'lat', 'Longitude': 'lon'})
        st.map(map_df)
    else:
        st.info("No users found for this city.")
else:
    st.error(f"Failed to fetch data. Status code: {response.status_code}")