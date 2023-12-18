# Introduction to Algorithmic Trading

Algorithmic trading is a method of executing orders using automated pre-programmed trading instructions accounting for variables such as time, price, and volume. This type of trading attempts to leverage the speed and computational resources of computers relative to human traders. In the twenty-first century, algorithmic trading has been gaining traction with both retail and institutional traders. 

It is widely used by investment banks, pension funds, mutual funds, and hedge funds that may need to spread out the execution of a larger order or perform trades too fast for human traders to react to. A study in 2019 showed that around 92% of trading in the Forex market was performed by trading algorithms rather than humans.

The term algorithmic trading is often used synonymously with automated trading system. These encompass a variety of trading strategies, some of which are based on formulas and results from mathematical finance, and often rely on specialized software.

Source : Wikipedia :)

## Bollinger Bands and Relative Strength Index (RSI)

### Mathematical background

#### Bollinger Bands

Let $x$ be serie of prices (generally closing price)

Here are the steps to follow to calculate the Bollinder Bands:

* Calculate the Moving Average over *n* period of x 
$$\mu = \frac{1}{n} \sum_{i}^n x_i $$
* Calculate the standard deviation as follow :
$$\sigma = \sqrt{\frac{1}{n} \sum_{i}^n (x_i - \mu)^2} $$
* Upper Band is :
$$\mu + \delta \sigma $$
* Lower Band is :
$$\mu - \delta \sigma $$

$\delta$ parameter could be adapted based on the analysis (1.5, 2, 2.5, ..)

##### Interpreation and use

The purpose of Bollinger Bands is to provide a relative definition of high and low prices of a market. By definition, prices are high at the upper band and low at the lower band.

The use of Bollinger Bands varies widely among traders. Some traders buy when price touches the lower Bollinger Band and exit when price touches the moving average in the center of the bands. Other traders buy when price breaks above the upper Bollinger Band or sell when price falls below the lower Bollinger Band.

#### Relative Strength Index

$$RSI = \frac{U(n)}{U(n) + D(n)} \times (100) $$

where :
* U : Exponential smoothed moving average of n-period of upward change 
* D : Exponential smoothed moving average of n-period of downward change 
* n : Period of moving average

##### Interpreation and use

Traditionally, RSI readings greater than the 70 level are considered to be in overbought territory, and RSI readings lower than the 30 level are considered to be in oversold territory. In between the 30 and 70 level is considered neutral, with the 50 level a sign of no trend.


## Strategy to implement

Here is the Strategy that needs to be implemented :
* If RSI < rsi_lower AND Closing Price < Lower Bollinger Band ==> BUY
* If RSI > rsi_lower AND Closing Price > Lower Bollinger Band ==> SELL
* Stop-Loss ==> If Closing Price < sl_percentage * Buy Price, ==> SELL
* Buy or Sell stock only one by one
* No Short selling


