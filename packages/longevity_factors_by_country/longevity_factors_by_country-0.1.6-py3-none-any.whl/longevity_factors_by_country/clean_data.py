from database.pg_connect import connect
import psycopg2
import pandas as pd 


engine, cursor = connect()


def replace_missing_with_avg(df, coeff):
    """
    Helper method: handles none values in a data frame by returning the average value for a country across all years
    Parameters
    ----------
    df: Pandas.DataFrame
    table: string

    Returns
    -------
    DataFrame
      DataFrame with no nones. 
    """
    #convert to numeric
    df[coeff] = pd.to_numeric(df[coeff])
    # Group by 'country' and calculate the average coefficient for each country
    avg_coefficients = df.groupby('country')[coeff].transform('mean')
    
    # Replace missing values in the 'coefficient' column with the corresponding country's average
    df[coeff] = df[coeff].fillna(avg_coefficients)
    return df

def getCoefficient(table): 
    """
    Helper method: returns coefficient for a given table
    Parameters
    ----------
    table: string

    Returns
    -------
    String
      Coefficient/column name that represents the dataframe.  

    """
    if table == "happiness":
        return "cantril_score"
    if table == "life_expectancy":
        return "lifespan"
    if table == "edu_spend":
        return "edu_spend_pc_gdp"
    if table == "health_spend":
        return "health_spend_pc_gdp"
    if table == "inequality":
        return "gini_coefficient"
    else: 
         raise Exception("Invalid table")

def getTables(cursor): 
    """
    Helper method: returns list of tables in the database

    Parameters
    ----------
    cursor: pymysql.connections.Connection

    Returns
    -------
    Array
      List of tables.  

    """
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    tables_output = cursor.fetchall()
    tables = [item[0] for item in tables_output if isinstance(item, tuple) and len(item) == 1 and isinstance(item[0], str)]
    return tables 

def getDataFrameForTable(sql, cursor):
    """
    Helper method: gathers data based on sql query

    Parameters
    ----------
    sql: string
      sql statement to execute
    cursor: pymysql.connections.Connection

    Returns
    -------
    pandas.DataFrame
      Dataframe for sql query results. 

    """
    df = pd.read_sql(sql, engine)
    return df

def getDataFrameRelevantYears(table, year, cursor):
    """
    Helper method: gathers data for input year, handles empty values

    Parameters
    ----------
    table: string
      table name to retrieve data from
    year: string
      desired year to query for
    cursor: pymysql.connections.Connection

    Returns
    -------
    pandas.DataFrame
      Dataframe filtered by desired year. 

    """
    sql = "SELECT * FROM " + table 
    df_orig = getDataFrameForTable(sql, cursor)
    coeff = getCoefficient(table)
    df = replace_missing_with_avg(df_orig, coeff)
    filtered_df = df[df["year"] == year]

    return filtered_df

def mergeDataFramesForCountryAndYear(df1, df2):
    """
    Helper method: merges dataframe based on country and year

    Parameters
    ----------
    df1: Pandas.DataFrame
      dataframe to merge
    df1: Pandas.DataFrame
      dataframe to merge

    Returns
    -------
    pandas.DataFrame
      dataframe containing join results. 

    """
    df = df1.merge(df2, how='inner', on=['country', 'year'])
    return df 

def getDataMerged(year, engine, cursor):
    """
    Merges data across all tables

    Parameters
    ----------
    year: string
      year to select for the data frame

    Returns
    -------
    pandas.DataFrame
      The data frame containing longevity data for a subset of countries for a given year. 

    """
    engine = engine 
    cursor = cursor
    tables_orig = getTables(cursor)
    df = getDataFrameRelevantYears('life_expectancy', year, cursor)

    tables = [item for item in tables_orig if item != 'life_expectancy']
    for table in tables:
        df1 = getDataFrameRelevantYears(table, year, cursor)
        df = mergeDataFramesForCountryAndYear(df, df1)
    return df
