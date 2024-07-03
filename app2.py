import streamlit as st
import investpy as ip
from datetime import datetime, timedelta
import plotly.graph_objs as go
from streamlit_autorefresh import st_autorefresh
from collections.abc import Iterable

# List of countries and intervals
countries = [
    "Argentina",
    "Australia",
    "Austria",
    "Bangladesh",
    "Belgium",
    "Bosnia",
    "Brazil",
    "Bulgaria",
    "Canada",
    "China",
    "Colombia",
    "Croatia",
    "Czech Republic",
    "Denmark",
    "Dubai",
    "Egypt",
    "Finland",
    "France",
    "Germany",
    "Greece",
    "Hong Kong",
    "Hungary",
    "Iceland",
    "India",
    "Indonesia",
    "Ireland",
    "Italy",
    "Ivory Coast",
    "Jamaica",
    "Japan",
    "Jordan",
    "Kazakhstan",
    "Kuwait",
    "Lebanon",
    "Malawi",
    "Malaysia",
    "Malta",
    "Mauritius",
    "Mexico",
    "Mongolia",
    "Montenegro",
    "Morocco",
    "Namibia",
    "Netherlands",
    "New Zealand",
    "Nigeria",
    "Norway",
    "Oman",
    "Pakistan",
    "Palestine",
    "Peru",
    "Philippines",
    "Poland",
    "Portugal",
    "Qatar",
    "Romania",
    "Russia",
    "Rwanda",
    "Saudi Arabia",
    "Serbia",
    "Singapore",
    "Slovenia",
    "South Africa",
    "South Korea",
    "Spain",
    "Sri Lanka",
    "Sweden",
    "Switzerland",
    "Taiwan",
    "Tanzania",
    "Tunisia",
    "Ukraine",
    "United Kingdom",
    "United States",
    "Venezuela",
    "Vietnam",
    "Zambia",
]
intervals = ["Daily", "Weekly", "Monthly"]

start_date = datetime.now() - timedelta(days=30)
end_date = datetime.now()


# Caching functions to avoid redundant data fetching
@st.cache_data()
def consultar_acao(stock, country, from_date, to_date, interval):
    df = ip.get_stock_historical_data(
        stock=stock,
        country=country,
        from_date=from_date,
        to_date=to_date,
        interval=interval,
    )
    return df


@st.cache_data()
def consultar_crypto(crypto, from_date, to_date, interval):
    df = ip.get_crypto_historical_data(
        crypto=crypto, from_date=from_date, to_date=to_date, interval=interval
    )
    return df


# Formatting date
def format_date(dt, format="%d/%m/%Y"):
    return dt.strftime(format)


# Plotting candlestick chart
def plotCandleStick(df, acao="ticket"):
    trace1 = {
        "x": df.index,
        "open": df.Open,
        "close": df.Close,
        "high": df.High,
        "low": df.Low,
        "type": "candlestick",
        "name": acao,
        "showlegend": False,
    }

    data = [trace1]
    layout = go.Layout()

    fig = go.Figure(data=data, layout=layout)
    return fig


# Creating the sidebar
barra_lateral = st.sidebar.empty()
country_select = st.sidebar.selectbox("Select country:", countries)
stocks = ip.get_stocks_list(country=country_select)
cryptos = ip.get_cryptos_list()
stock_select = st.sidebar.selectbox("Select the stock:", stocks)
crypto_select = st.sidebar.selectbox("Select the Cryptocurrency:", cryptos)
from_date = st.sidebar.date_input("Start Date:", start_date)
to_date = st.sidebar.date_input("End Date:", end_date)
interval_select = st.sidebar.selectbox("Select the range:", intervals)
carregar_dados = st.sidebar.checkbox("Load Data")

grafico_line = st.empty()
grafico_candle = st.empty()

# Central page elements
st.title("Stock Monitor")
st.header("Stocks")
st.subheader("Graphical visualization")

# Error handling for date input
if from_date > to_date:
    st.sidebar.error("Data de ínicio maior do que data final")
else:
    df = consultar_crypto(
        crypto_select, format_date(from_date), format_date(to_date), interval_select
    )
    try:
        fig = plotCandleStick(df)
        grafico_candle = st.plotly_chart(fig)
        grafico_line = st.line_chart(df.Close)
        if carregar_dados:
            st.subheader("Dados")
            dados = st.dataframe(df)
    except Exception as e:
        st.error(e)

# Auto-refresh functionality
count = st_autorefresh(interval=5000, limit=10000, key="fizzbuzzcounter")

if count == 0:
    st.write("Count is zero")
elif count % 3 == 0 and count % 5 == 0:
    st.write("FizzBuzz")
elif count % 3 == 0:
    st.write("Fizz")
elif count % 5 == 0:
    st.write("Buzz")
else:
    st.write(f"Count: {count}")
