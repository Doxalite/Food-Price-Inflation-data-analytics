import streamlit as st
import pandas as pd
from visualisation import plot_cpi_food_index, plot_cpi_food_index_income_sg, plot_cpi_food_index_income_us
import time

data = pd.read_csv('data.csv')
data.head()

data.sort_values(by='date', inplace=True, ascending=True)
data['date'] = pd.to_datetime(data['date'])
if 'year_graph1' not in st.session_state:
    st.session_state['year_graph1'] = 0
if 'year_graph2' not in st.session_state:
    st.session_state['year_graph2'] = 0
if 'year_graph3' not in st.session_state:
    st.session_state['year_graph3'] = 0


st.title("Food Price Inflation Analysis")

st.markdown("<small>All Indexes have year 2000 as base period<small>", unsafe_allow_html=True)

st.subheader("CPI and Food Inflation Index over Time for US and SG")

# plot initial graph
chart_placeholder1 = st.empty()
with chart_placeholder1, st.spinner("Loading chart..."):
    cpi_food_index_fig = plot_cpi_food_index(data, st.session_state['year_graph1'])
chart_placeholder1.pyplot(cpi_food_index_fig)

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("1 year", key="11"):
        st.session_state['year_graph1'] = 1
with col2:
    if st.button("2 years", key="12"):
        st.session_state['year_graph1'] = 2
with col3:
    if st.button("5 years", key="13"):
        st.session_state['year_graph1'] = 5
with col4:
    if st.button("10 years", key="14"):
        st.session_state['year_graph1'] = 10
with col5:
    if st.button("Max", key="15"):
        st.session_state['year_graph1'] = 0

with chart_placeholder1, st.spinner("Loading chart..."):
    time.sleep(2)
    cpi_food_index_fig = plot_cpi_food_index(data, st.session_state['year_graph1'])
chart_placeholder1.pyplot(cpi_food_index_fig)

st.subheader("CPI, Food Inflation Index compared to Income for SG")

chart_placeholder2 = st.empty()
cpi_food_index_income_sg_fig = plot_cpi_food_index_income_sg(data, st.session_state['year_graph2'])
chart_placeholder2.pyplot(cpi_food_index_income_sg_fig)

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("1 year", key="21"):
        st.session_state['year_graph2'] = 1
with col2:
    if st.button("2 years", key="22"):
        st.session_state['year_graph2'] = 2
with col3:
    if st.button("5 years", key="23"):
        st.session_state['year_graph2'] = 5
with col4:
    if st.button("10 years", key="24"):
        st.session_state['year_graph2'] = 10
with col5:
    if st.button("Max", key="25"):
        st.session_state['year_graph2'] = 0

with chart_placeholder2, st.spinner("Loading chart..."):
    cpi_food_index_income_sg_fig = plot_cpi_food_index_income_sg(data, st.session_state['year_graph2'])
chart_placeholder2.pyplot(cpi_food_index_income_sg_fig)

st.subheader("CPI, Food Inflation Index compared to Income for US")

chart_placeholder3 = st.empty()
cpi_food_index_income_us_fig = plot_cpi_food_index_income_us(data, st.session_state['year_graph3'])
chart_placeholder3.pyplot(cpi_food_index_income_us_fig)

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("1 year", key="31"):
        st.session_state['year_graph3'] = 1
with col2:
    if st.button("2 years", key="32"):
        st.session_state['year_graph3'] = 2
with col3:
    if st.button("5 years", key="33"):
        st.session_state['year_graph3'] = 5
with col4:
    if st.button("10 years", key="34"):
        st.session_state['year_graph3'] = 10
with col5:
    if st.button("Max", key="35"):
        st.session_state['year_graph3'] = 0

with chart_placeholder3, st.spinner("Loading chart..."):
    cpi_food_index_income_us_fig = plot_cpi_food_index_income_us(data, st.session_state['year_graph3'])
chart_placeholder3.pyplot(cpi_food_index_income_us_fig)

df = pd.read_csv('prediction_2026.csv', index_col=0)
CPI_prediction_2026 = round(df.loc[:,'CPI'].values[0], 2)
inflation_prediction_2026 = df.loc[:,'Inflation Rate'].values[0]
st.subheader("Prediction for 2026")

st.write(f'2026 CPI prediction: {CPI_prediction_2026}')
st.write(f'with 2000 as base year')
st.write(f'Predicted inflation rate: {inflation_prediction_2026}%')