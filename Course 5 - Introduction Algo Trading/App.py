import streamlit as st
from Strategy import Strategy_1
from Performance import Performance_calculator
import matplotlib.pyplot as plt

st.title('Introduction to algorithmic Trading using Python')


ticker = st.sidebar.text_input('Please enter a Ticker to test the strategy', value = 'SQ')
start = st.sidebar.text_input('Select a starting date', value = '2019-01-01')
end = st.sidebar.text_input('Select an ending date', value='2022-08-13')
bb_period = st.sidebar.number_input('Choose a moving average period for BB', value = 20)
rsi_period = st.sidebar.number_input('Choose a moving average period for RSI', value = 7)
stop_loss = st.sidebar.checkbox('Stop Loss ?')
if stop_loss:
    stop_loss_value = st.sidebar.number_input('Please choose a level of stop loss to apply', value = 0.95)
    output = Strategy_1(ticker, start, end, bb_period, rsi_period, stop_loss, stop_loss_value)
else:
    output = Strategy_1(ticker, start, end, bb_period, rsi_period, stop_loss)


st.line_chart(output['df'][['Close', 'ma_20', 'upper_bb', 'lower_bb']])

fig, ax = plt.subplots()
ax = plt.plot(output['df'].Close)
ax = plt.scatter(output['df'].loc[output['buydates']].index,
                output['df'].loc[output['buydates']].Close,
                marker = '^', c = 'g')
ax = plt.scatter(output['df'].loc[output['selldates']].index,
                output['df'].loc[output['selldates']].Close,
                marker = 'v', c = 'r')
st.pyplot(fig)
return_start = Performance_calculator(output['buyprices'], output['sellprices'])

st.write(f"Your strategy gave you {return_start} % as return !")