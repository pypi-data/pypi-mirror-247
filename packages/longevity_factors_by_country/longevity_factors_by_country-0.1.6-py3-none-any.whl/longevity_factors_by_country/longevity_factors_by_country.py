import pandas as pd
from clean_data import getDataMerged
from database.pg_connect import connect

df = pd.DataFrame()

def getLongevityDataForYear(year):
    """
    Retrieves Longevity Data for a given year

    Parameters
    ----------
    year: string
      A pandas categorical.

    Returns
    -------
    pandas.DataFrame
      The data frame containing longevity data for a subset of countries for a given year. 

    """
    engine, cursor = connect()
    df = getDataMerged(year, engine, cursor)
    #returns a dataframe of lifespan
    return df

def getCountriesWithTopLifeSpan(df, n): 
    """
    Retrieves Longevity Data for countries with the n longest lifespans 

    Parameters
    ----------
    df: pandas.DataFrame
      Initial Country data frame returned from getLongevityData 
    n: integer
      number of values to return 
    Returns
    -------
    pandas.DataFrame
      The data frame containing longevity data for a subset of countries for a given year with n longest lifespans. 

    """
    return df.nlargest(n, "lifespan")

def getCountriesWithLowestLifeSpan(df, n):
    """
    Retrieves Longevity Data for countries with the n lowest lifespans 

    Parameters
    ----------
    df: pandas.DataFrame
      Initial Country data frame returned from getLongevityData 
    n: integer
      number of values to return 
    Returns
    -------
    pandas.DataFrame
      The data frame containing longevity data for a subset of countries for a given year with n lowest lifespans. 

    """
    return df.nsmallest(n, "lifespan")

def writeCSV(year):
  df = getLongevityDataForYear(year)
  df.to_csv(year+" Longevity Data")


writeCSV(year= "2019")