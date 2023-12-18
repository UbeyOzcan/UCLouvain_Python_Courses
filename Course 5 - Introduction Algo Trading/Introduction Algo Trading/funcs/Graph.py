import plotly.graph_objects as go


def plot_startegy(strategy_result, rsi_l, rsi_u):
    fig = strategy_result['df'][['Close', 'ma_n', 'upper_bb', 'lower_bb']].plot(
        title="Close, moving average, upper bb, lower bb graph", template="simple_white",
        labels=dict(index="time", value="Prices", variable="Metric"))

    fig2 = strategy_result['df'][['rsi']].plot(title="RSI graph", template="simple_white",
                                               labels=dict(index="time", value="Prices", variable="Metric"))
    fig2.add_hline(y=rsi_l, line_width=3, line_dash="dash", line_color="green")
    fig2.add_hline(y=rsi_u, line_width=3, line_dash="dash", line_color="green")

    fig3 = strategy_result['df'].Open.plot(title="Open price and signals", template="simple_white",
                                            labels=dict(index="time", value="Prices", variable="Metric"))

    fig3 = fig3.add_trace(go.Scatter(x=strategy_result['df'].loc[strategy_result['buydates']].index,
                                     y=strategy_result['df'].loc[strategy_result['buydates']].Close,
                                     marker_symbol='arrow-up',
                                     mode='markers',
                                     marker=dict(
                                         color='Green',
                                         size=20
                                     ), showlegend=False)
                          )

    fig3 = fig3.add_trace(go.Scatter(x=strategy_result['df'].loc[strategy_result['selldates']].index,
                                     y=strategy_result['df'].loc[strategy_result['selldates']].Close,
                                     marker_symbol='arrow-down',
                                     mode='markers',
                                     marker=dict(
                                         color='red',
                                         size=20
                                     ), showlegend=False)
                          )

    return fig, fig2, fig3