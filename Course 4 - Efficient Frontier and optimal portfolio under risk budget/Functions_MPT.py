import yfinance as yf
import numpy as np
import datetime as dt
import scipy.optimize as sc
import plotly.graph_objects as go
import pandas as pd


# Import data
def getData(stocks, start, end):
    prices = pd.DataFrame()
    for i in stocks:
        prices = pd.concat([prices, pd.DataFrame(yf.download(i, start, end)["Close"])], axis=1)
    prices.columns = stocks
    returns = prices.pct_change()
    meanReturns = returns.mean()
    covMatrix = returns.cov()
    return prices, returns, meanReturns, covMatrix


def portfolioPerformance(weights, meanReturns, covMatrix):
    returns = np.sum(meanReturns * weights) * 252
    std = np.sqrt(
        np.dot(weights.T, np.dot(covMatrix, weights))
    ) * np.sqrt(252)
    return returns, std


def negativeSR(weights, meanReturns, covMatrix, riskFreeRate=0):
    pReturns, pStd = portfolioPerformance(weights, meanReturns, covMatrix)
    return - (pReturns - riskFreeRate) / pStd


def maxSR(meanReturns, covMatrix, riskFreeRate=0, constraintSet=(0, 1)):
    "Minimize the negative SR, by altering the weights of the portfolio"
    numAssets = len(meanReturns)
    args = (meanReturns, covMatrix, riskFreeRate)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bound = constraintSet
    bounds = tuple(bound for asset in range(numAssets))
    result = sc.minimize(negativeSR, numAssets * [1. / numAssets], args=args,
                         method='SLSQP', bounds=bounds, constraints=constraints)
    return result


def portfolioVariance(weights, meanReturns, covMatrix):
    return portfolioPerformance(weights, meanReturns, covMatrix)[1]


def minimizeVariance(meanReturns, covMatrix, constraintSet=(0, 1)):
    """Minimize the portfolio variance by altering the 
     weights/allocation of assets in the portfolio"""
    numAssets = len(meanReturns)
    args = (meanReturns, covMatrix)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bound = constraintSet
    bounds = tuple(bound for asset in range(numAssets))
    result = sc.minimize(portfolioVariance, numAssets * [1. / numAssets], args=args,
                         method='SLSQP', bounds=bounds, constraints=constraints)
    return result


def portfolioReturn(weights, meanReturns, covMatrix):
    return portfolioPerformance(weights, meanReturns, covMatrix)[0]


def efficientOpt(meanReturns, covMatrix, returnTarget, constraintSet=(0, 1)):
    """For each returnTarget, we want to optimise the portfolio for min variance"""
    numAssets = len(meanReturns)
    args = (meanReturns, covMatrix)

    constraints = ({'type': 'eq', 'fun': lambda x: portfolioReturn(x, meanReturns, covMatrix) - returnTarget},
                   {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bound = constraintSet
    bounds = tuple(bound for asset in range(numAssets))
    effOpt = sc.minimize(portfolioVariance, numAssets * [1. / numAssets], args=args, method='SLSQP', bounds=bounds,
                         constraints=constraints)
    return effOpt


def calculatedResults(meanReturns, covMatrix, riskFreeRate=0, constraintSet=(0, 1)):
    """Read in mean, cov matrix, and other financial information
        Output, Max SR , Min Volatility, efficient frontier """
    # Max Sharpe Ratio Portfolio
    maxSR_Portfolio = maxSR(meanReturns, covMatrix)
    maxSR_returns, maxSR_std = portfolioPerformance(maxSR_Portfolio['x'], meanReturns, covMatrix)
    maxSR_allocation = pd.DataFrame(maxSR_Portfolio['x'], index=meanReturns.index, columns=['allocation'])
    maxSR_allocation.allocation = [round(i * 100, 0) for i in maxSR_allocation.allocation]

    # Min Volatility Portfolio
    minVol_Portfolio = minimizeVariance(meanReturns, covMatrix)
    minVol_returns, minVol_std = portfolioPerformance(minVol_Portfolio['x'], meanReturns, covMatrix)
    minVol_allocation = pd.DataFrame(minVol_Portfolio['x'], index=meanReturns.index, columns=['allocation'])
    minVol_allocation.allocation = [round(i * 100, 0) for i in minVol_allocation.allocation]

    # Efficient Frontier
    efficientList = []
    targetReturns = np.linspace(minVol_returns, maxSR_returns*1.1, 20)
    for target in targetReturns:
        efficientList.append(efficientOpt(meanReturns, covMatrix, target)['fun'])

    maxSR_returns, maxSR_std = round(maxSR_returns * 100, 2), round(maxSR_std * 100, 2)
    minVol_returns, minVol_std = round(minVol_returns * 100, 2), round(minVol_std * 100, 2)
    return maxSR_returns, maxSR_std, maxSR_allocation, minVol_returns, minVol_std, minVol_allocation, efficientList, targetReturns


def simulate(stocks, meanReturns, covMatrix, n_sim, riskFreeRate=0):
    numAssets = len(meanReturns)
    simulated_ptf_return = []
    simulated_ptf_std = []
    simulated_sharpe_ratio = []
    w = np.zeros((n_sim, numAssets))
    portfolio = pd.DataFrame()
    for i in np.arange(n_sim):
        weights = np.array(np.random.random(numAssets))
        weights = weights / np.sum(weights)
        simulated_ptf_return.append(np.sum(weights * meanReturns) * 252)
        simulated_ptf_std.append(np.sqrt(
            np.dot(weights.T, np.dot(covMatrix, weights))) * np.sqrt(252))
        simulated_sharpe_ratio.append((simulated_ptf_return[i] - np.array(riskFreeRate)) / simulated_ptf_std[i])
        w[i, :] = weights
    for i in range(numAssets):
        if i == 0:
            portfolio = pd.DataFrame({stocks[i]: w[:, i]})
        else:
            portfolio[stocks[i]] = w[:, i]
    portfolio['Return'] = simulated_ptf_return
    portfolio['Volatility'] = simulated_ptf_std
    portfolio['Sharpe Ratio'] = simulated_sharpe_ratio
    return portfolio


def EF_graph(stocks, n_sim, meanReturns, covMatrix, riskFreeRate=0, constraintSet=(0, 1)):
    """Return a graph ploting the min vol, max sr and efficient frontier"""
    maxSR_returns, maxSR_std, maxSR_allocation, minVol_returns, minVol_std, minVol_allocation, efficientList, targetReturns = calculatedResults(
        meanReturns, covMatrix, riskFreeRate, constraintSet)
    portfolio = simulate(stocks, meanReturns, covMatrix, n_sim)

    # Efficient Frontier
    EF_curve = go.Scatter(
        name='Efficient Frontier',
        mode='lines',
        x=[round(ef_std * 100, 2) for ef_std in efficientList],
        y=[round(target * 100, 2) for target in targetReturns],
        line=dict(color='black', width=4, dash='dashdot')
    )

    # Max SR
    MaxSharpeRatio = go.Scatter(
        name='Maximium Sharpe Ratio',
        mode='markers',
        x=[maxSR_std],
        y=[maxSR_returns],
        marker=dict(color='red', size=14, line=dict(width=3, color='black'))
    )

    # Min Vol
    MinVol = go.Scatter(
        name='Mininium Volatility',
        mode='markers',
        x=[minVol_std],
        y=[minVol_returns],
        marker=dict(color='green', size=14, line=dict(width=3, color='black'))
    )


    #Simulated Portfolio
    sim_plot = go.Scatter(
        name='Simulate Ptfs',
        mode='markers',
        x=round(portfolio['Volatility'] * 100, 2),
        y=round(portfolio['Return'] * 100, 2),
        marker=dict(
            color=round(portfolio['Sharpe Ratio'] * 100, 2),
            showscale=True
        )

    )

    data = [MaxSharpeRatio, MinVol, EF_curve, sim_plot]

    layout = go.Layout(
        title='Portfolio Optimisation with the Efficient Frontier',
        yaxis=dict(title='Annualised Return (%)'),
        xaxis=dict(title='Annualised Volatility (%)'),
        showlegend=True,
        legend=dict(
            x=0.75, y=0, traceorder='normal',
            bgcolor='#E2E2E2',
            bordercolor='black',
            borderwidth=2),
        width=800,
        height=600)

    fig = go.Figure(data=data, layout=layout)
    return fig.show()
