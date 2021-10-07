import streamlit as st
import investpy as ip
from datetime import datetime, timedelta
import plotly.graph_objs as go
from streamlit_autorefresh import st_autorefresh


countries = ['Argentina',
             'Australia', 'Austria', 'Bangladesh',
             'Belgium',
             'Bosnia', 'Brazil', 'Bulgaria',
             'Canada', 'China', 'Colombia', 'Croatia', 'Czech Republic', 'Denmark', 'Dubai', 'Egypt',
             'Finland', 'France', 'Germany', 'Greece', 'Hong Kong', 'Hungary', 'Iceland', 'India',
             'Indonesia', 'Ireland', 'Italy', 'Ivory Coast', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan',
             'Kuwait', 'Lebanon', 'Malawi', 'Malaysia', 'Malta', 'Mauritius', 'Mexico', 'Mongolia',
             'Montenegro', 'Morocco', 'Namibia', 'Netherlands', 'New Zealand', 'Nigeria',  'Norway',
             'Oman', 'Pakistan', 'Palestine',  'Peru',  'Philippines', 'Poland', 'Portugal', 'Qatar',
             'Romania', 'Russia', 'Rwanda',  'Saudi Arabia', 'Serbia', 'Singapore', 'Slovenia',
             'South Africa', 'South Korea', 'Spain',  'Sri Lanka', 'Sweden', 'Switzerland', 'Taiwan',
             'Tanzania', 'Tunisia', 'Ukraine', 'United Kingdom', 'United States', 'Venezuela',
             'Vietnam', 'Zambia']

intervals = ['Daily', 'Weekly', 'Monthly']

start_date = datetime.today()-timedelta(days=30)
end_date = datetime.today()


@st.cache(allow_output_mutation=True)
def consultar_acao(stock, country, from_date, to_date, interval):
    df = ip.get_stock_historical_data(
        stock=stock, country=country, from_date=from_date,
        to_date=to_date, interval=interval)
    return df


def format_date(dt, format='%d/%m/%Y'):
    return dt.strftime(format)


def plotCandleStick(df, acao='ticket'):
    trace1 = {
        'x': df.index,
        'open': df.Open,
        'close': df.Close,
        'high': df.High,
        'low': df.Low,
        'type': 'candlestick',
        'name': acao,
        'showlegend': False
    }

    data = [trace1]
    layout = go.Layout()

    fig = go.Figure(data=data, layout=layout)
    return fig


# CRIANDO UMA BARRA LATERAL
barra_lateral = st.sidebar.empty()
country_select = st.sidebar.selectbox("Select country:", countries)
stocks = ip.get_stocks_list(country=country_select)
stock_select = st.sidebar.selectbox("Select the stock:", stocks)
from_date = st.sidebar.date_input('Start Date:', start_date)
to_date = st.sidebar.date_input('End Date:', end_date)
interval_select = st.sidebar.selectbox("Select the range:", intervals)
carregar_dados = st.sidebar.checkbox('Load Data')


grafico_line = st.empty()
grafico_candle = st.empty()

# elementos centrais da página
st.title('Stock Monitor')

st.header('Stocks')

st.subheader('Graphical visualization')


if from_date > to_date:
    st.sidebar.error('Data de ínicio maior do que data final')
else:
    df = consultar_acao(stock_select, country_select, format_date(
        from_date), format_date(to_date), interval_select)
    try:
        fig = plotCandleStick(df)
        grafico_candle = st.plotly_chart(fig)
        grafico_line = st.line_chart(df.Close)
        if carregar_dados:
            st.subheader('Dados')
            dados = st.dataframe(df)
            stock_select = st.sidebar.selectbox
    except Exception as e:
        st.error(e)


# Run the autorefresh about every 2000 milliseconds (2 seconds) and stop
# after it's been refreshed 100 times.
count = st_autorefresh(interval=5000, limit=10000, key="fizzbuzzcounter")

# The function returns a counter for number of refreshes. This allows the
# ability to make special requests at different intervals based on the count
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
