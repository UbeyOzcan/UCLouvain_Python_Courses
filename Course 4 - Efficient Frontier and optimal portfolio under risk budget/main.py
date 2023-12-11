import matplotlib.pyplot as plt
from Functions_MPT import *
import datetime as dt

my_ptf = ['CBA.AX', 'BHP.AX', 'TLS.AX']

endDate = dt.datetime.now()
startDate = endDate - dt.timedelta(days=365)

prices, returns, meanReturns, covMatrix = getData(stocks=my_ptf,
                                                  start=startDate,
                                                  end=endDate)
#print(simulate(my_ptf, meanReturns, covMatrix, 100))

EF_graph(stocks=my_ptf,
         n_sim=1000,
         meanReturns=meanReturns,
         covMatrix=covMatrix)
