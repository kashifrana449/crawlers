from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

import settings

# Base
Base = declarative_base()

# sports session
mysql_engine_sports = create_engine(settings.MYSQL_DB_URI.format(**settings.MYSQL_DB_SPORTS), encoding='utf8')
mysql_session_sports = scoped_session(sessionmaker(bind=mysql_engine_sports,
                                                   autocommit=False,
                                                   autoflush=False,
                                                   expire_on_commit=True))

# Real Estate session
mysql_engine_real_estate = create_engine(settings.MYSQL_DB_URI.format(**settings.MYSQL_DB_REAL_ESTATE), encoding='utf8')
mysql_session_real_estate = scoped_session(sessionmaker(bind=mysql_engine_real_estate,
                                                        autocommit=False,
                                                        autoflush=False,
                                                        expire_on_commit=True))
# country_stats session
mysql_engine_country_stats = create_engine(settings.MYSQL_DB_URI.format(**settings.MYSQL_DB_COUNTRY_STATS),
                                           encoding='utf8')
mysql_session_country_stats = scoped_session(sessionmaker(bind=mysql_engine_country_stats,
                                                          autocommit=False,
                                                          autoflush=False,
                                                          expire_on_commit=True))

# crime session
mysql_engine_crime = create_engine(settings.MYSQL_DB_URI.format(**settings.MYSQL_DB_CRIME),
                                   encoding='utf8')
mysql_session_crime = scoped_session(sessionmaker(bind=mysql_engine_crime,
                                                  autocommit=False,
                                                  autoflush=False,
                                                  expire_on_commit=True))

# Big Data session
mysql_engine_big_data = create_engine(settings.MYSQL_DB_URI.format(**settings.MYSQL_DB_BIG_DATA),
                                      encoding='utf8')
mysql_session_big_data = scoped_session(sessionmaker(bind=mysql_engine_big_data,
                                                     autocommit=False,
                                                     autoflush=False,
                                                     expire_on_commit=True))

