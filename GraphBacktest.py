from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import pandas as pd


def graph(network,Adress,fromdate):

    if network == 1:

        sample_transport=RequestsHTTPTransport(
        url='https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3',
        verify=True,
        retries=5,
        )
        client = Client(
        transport=sample_transport
        )


    elif network == 2:
       
        sample_transport=RequestsHTTPTransport(
        url='https://api.thegraph.com/subgraphs/name/ianlapham/uniswap-arbitrum-one',
        verify=True,
        retries=5,
        )
        client = Client(
        transport=sample_transport
        )

    elif network == 3:
        sample_transport=RequestsHTTPTransport(
        url='https://api.thegraph.com/subgraphs/name/ianlapham/uniswap-optimism-dev',
        verify=True,
        retries=5,
        )
        client = Client(
        transport=sample_transport
        )
    print(fromdate)

    query = gql('''
    query ($fromdate: Int!)
    {
    poolHourDatas(where:{pool:"'''+str(Adress)+'''",periodStartUnix_gt:$fromdate},orderBy:periodStartUnix,orderDirection:desc,first:1000)
    {
    periodStartUnix
    liquidity
    high
    low
    pool{
        
        totalValueLockedUSD
        totalValueLockedToken1
        totalValueLockedToken0
        token0
            {decimals
            }
        token1
            {decimals
            }
        }
    close
    feeGrowthGlobal0X128
    feeGrowthGlobal1X128
    }
 
    }
    ''')
    params = {
    "fromdate": fromdate
    }

    response = client.execute(query,variable_values=params)
    dpd =pd.json_normalize(response['poolHourDatas'])
    dpd=dpd.astype(float)
    return dpd

