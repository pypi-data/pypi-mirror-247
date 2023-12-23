from pg_connect import connect
import psycopg2

#this file is meant to be run as a script TODO fix this so it's using engine 
# Connecting to DB
engine, cursor = connect()

# SQL command to show inventory 
show_tables = """
SELECT * FROM pg_catalog.pg_tables WHERE schemaname='public'
    """

# Execute SQL Command to create tables and commit to DB

create_lifespan_table = """
CREATE TABLE LIFE_EXPECTANCY(
    ENTITY VARCHAR(255),
    CODE VARCHAR(255),
    YEAR VARCHAR(255),
    LIFESPAN VARCHAR(255),                                                                                                    
);

"""

create_inequality_table = """
CREATE TABLE INEQUALITY(
    COUNTRY VARCHAR(255),
    YEAR VARCHAR(255),
    GINI_COEFFICIENT VARCHAR(255)                                                                                                  
);
"""
create_happiness_table = """
CREATE TABLE HAPPINESS(
    COUNTRY VARCHAR(255),
    YEAR VARCHAR(255),
    CANTRIL_SCORE VARCHAR(255)                                                                                                  
);
"""
create_health_spend_table = """
CREATE TABLE HEALTH_SPEND(
    COUNTRY VARCHAR(255),
    CODE VARCHAR(255),
    YEAR VARCHAR(255),
    HEALTH_SPEND_PC_GDP VARCHAR(255)                                                                                                    
);
"""

create_edu_spend_table = """
CREATE TABLE EDU_SPEND(
    COUNTRY VARCHAR(255),
    CODE VARCHAR(255),
    YEAR VARCHAR(255),
    EDU_SPEND_PC_GDP VARCHAR(255)                                                                                                    
);
"""
cursor.execute(create_edu_spend_table)
cursor.execute(create_health_spend_table)
cursor.execute(create_happiness_table)
cursor.execute(create_inequality_table)

print(cursor.execute(show_tables))
engine.commit()


# Disconnect from DB
engine.close()