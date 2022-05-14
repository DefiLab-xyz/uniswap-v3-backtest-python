import pandas as pd


def chart1(dpd,base,myliquidity):

    if base==0:
        dpd['feeV']= (dpd['myfee0'] )+ (dpd['myfee1']* dpd['close'])
        dpd['amountV']= (dpd['amount0'] ) + (dpd['amount1']* dpd['close'])
        dpd['amountunb']= (dpd['amount0unb'] )+ (dpd['amount1unb']* dpd['close'])
        dpd['fgV']= (dpd['fee0token'])+ (dpd['fee1token']* dpd['close'])
        dpd['feeusd']= dpd['feeV'] * (dpd['pool.totalValueLockedUSD'].iloc[0] / (dpd['pool.totalValueLockedToken1'].iloc[0]* dpd['close'].iloc[0]+(dpd['pool.totalValueLockedToken0'].iloc[0])))


    else:

        dpd['feeV']= (dpd['myfee0'] / dpd['close']) + dpd['myfee1']
        dpd['amountV']= (dpd['amount0'] / dpd['close'])+ dpd['amount1']
        dpd['feeVbase0']= dpd['myfee0'] + (dpd['myfee1']* dpd['close'])
        dpd['amountunb']= (dpd['amount0unb'] / dpd['close'])+ dpd['amount1unb']
        dpd['fgV']=(dpd['fee0token'] / dpd['close'])+ dpd['fee1token']
        dpd['feeusd']= dpd['feeV'] * ( dpd['pool.totalValueLockedUSD'].iloc[0] / (dpd['pool.totalValueLockedToken1'].iloc[0] + (dpd['pool.totalValueLockedToken0'].iloc[0]/dpd['close'].iloc[0])))

    dpd['date']=pd.to_datetime(dpd['periodStartUnix'],unit='s')

    # 1 Chart
    
    #dpd['fgV']= (dpd['fg0'] / dpd['close'].iloc[0] + dpd['fg1'])
    #rint(dpd['fg1']/dpd['amount1unb'])

    data=dpd[['date','myfee0','myfee1','fgV','feeV','feeusd','amountV','ActiveLiq','amountunb','amount0','amount1','close']]
    data=data.fillna(0)

    temp =  data.resample('D',on='date').sum()
    final1=temp[['myfee0','myfee1','feeV','fgV','feeusd']].copy()

    temp2 = data.resample('D',on='date').mean()
    final1['ActiveLiq']=temp2['ActiveLiq'].copy()
    
    temp3 = data.resample('D',on='date').first()
    final1[['amountV','amountunb']]=temp3[['amountV','amountunb']].copy()
    temp4 = data.resample('D',on='date').last()
    final1[['amountVlast']]=temp4[['amountV']]

    final1['S1%']=final1['feeV']/final1['amountV']*100#*365
    final1['unb%']=final1['fgV']/final1['amountunb']*100#*365
    final1['multiplier']=final1['S1%']/final1['unb%']
    final1['feeunb'] = final1['amountV']*final1['unb%']/100
    final1.to_csv("chart1.csv",sep = ";")
    
    print(final1[['feeunb','feeV','feeusd','amountV','ActiveLiq','S1%','unb%','ActiveLiq']])

    print('------------------------------------------------------------------')
    print("this position returned", final1['feeV'].sum()/final1['amountV'].iloc[0]*100,"in ",len(final1.index)," days, for an apr of ",final1['feeV'].sum()/final1['amountV'].iloc[0]*365/len(final1.index)*100)
    print("a base  position returned", final1['feeunb'].sum()/final1['amountV'].iloc[0]*100,"in ",len(final1.index)," days, for an apr of ",final1['feeunb'].sum()/final1['amountV'].iloc[0]*365/len(final1.index)*100)
    
    print ("fee in token 1 and token 2",dpd['myfee0'].sum(),dpd['myfee1'].sum() )
    print("totalFee in USD", final1['feeusd'].sum())
    print ('Your liquidity was active for:',final1['ActiveLiq'].mean())
    forecast= (dpd['feeVbase0'].sum()*myliquidity*final1['ActiveLiq'].mean())
    print(dpd['feeVbase0'])
    print('forecast: ',forecast)
    print('------------------------------------------------------------------')
    # 1 chart e' completo
    
    # 2 chart

    
    final2=temp3[['amountV','amount0','amount1','close']].copy()
    final2['feeV']=temp['feeV'].copy()
    final2[['amountVlast']]=temp4[['amountV']]
    


    final2['HODL']=final2['amount0'].iloc[0] / final2['close'] + final2['amount1'].iloc[0]
    
    final2['IL']=final2['amountVlast']- final2['HODL']
    final2['ActiveLiq']=temp2['ActiveLiq'].copy()
    final2['feecumsum']=final2['feeV'].cumsum()
    final2 ['PNL']= final2['feecumsum'] + final2['IL']#-Bfinal['gas']

    final2['HODLnorm']=final2['HODL']/final2['amountV'].iloc[0]*100
    final2['ILnorm']=final2['IL']/final2['amountV'].iloc[0]*100
    final2['PNLnorm']=final2['PNL']/final2['amountV'].iloc[0]*100
    final2['feecumsumnorm'] = final2['feecumsum']/final2['amountV'].iloc[0]*100
    ch2=final2[['amountV','feecumsum']]
    ch3=final2[['ILnorm','PNLnorm','feecumsumnorm']]

    final2.to_csv("chart2.csv",sep = ";")
    print(ch2)
    print(ch3)

    #final3=data
    final3=pd.DataFrame()
    final3['amountV']=data['amountV']

    final3['amountVlast']=data['amountV'].shift(-1)
    final3['date']=data['date']
    final3['HODL']=data['amount0'].iloc[0] / data['close'] + data['amount1'].iloc[0]

    final3['amountVlast'].iloc[-1]=final3['HODL'].iloc[-1]
    final3['IL']=final3['amountVlast']- final3['HODL']
    final3['feecumsum']=data['feeV'][::-1].cumsum()
    final3 ['PNL']= final3['feecumsum'] + final3['IL']
    final3['HODLnorm']=final3['HODL']/final3['amountV'].iloc[0]*100
    final3['ILnorm']=final3['IL']/final3['amountV'].iloc[0]*100
    final3['PNLnorm']=final3['PNL']/final3['amountV'].iloc[0]*100
    final3['feecumsumnorm'] = final3['feecumsum']/final3['amountV'].iloc[0]*100

    ch2=final3[['amountV','feecumsum']]
    ch3=final3[['ILnorm','PNLnorm','feecumsumnorm']]


    print(ch2)
    print(ch3)



   
    
   

    

    