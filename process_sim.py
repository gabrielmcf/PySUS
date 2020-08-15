from pysus.online_data.SIM import download
from pysus.preprocessing.decoders import translate_variables_SIM, group_and_count, redistribution
from pysus.utilities import BR_STATES
import numpy as np
import pandas as pd
import csv

# A ordem das variáveis define a prioridade para distribuição.
# ['CODMUNRES','SEXO','IDADE_ANOS'] significa que IDADE_ANOS será removida primeiro na redistribuição e CODMUNRES por último.
variables = ['CODMUNRES','SEXO','IDADE_ANOS']
# folder = '/media/gabriel/Croquete/FTP_DATASUS/datasus/dissemin/publicos/SIM/CID10/DORES'

print("Baixando dados")
# years = [1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018]
# years = [1979,1980,1981,1982,1983,1984,1985,1986,1987,1988,1989,1990,1991,1992,1993,1994,1995]
# years = [1989,1990,1991,1992,1993,1994,1995]
years = list(range(2000,2011))
first = True
for state in ['SP']:
    for year in years:
        print("Baixando {} {}".format(state,year))
        df = download(state, year)

        print("Traduzindo variáveis")
        df = translate_variables_SIM(df,age_classes=True,classify_args={})

        print("Filtrando")
        df = df[variables]

        print("Agrupando e contando")
        count = group_and_count(df,variables)

        count = redistribution(count,variables)

        print("Adicionando colunas de ano e estado")
        count.insert(loc=0,column="UF",value=state)
        count.insert(loc=0,column="ANO",value=year)

        print("Salvando no CSV")
        # count.to_csv("SP-{}-{}.csv".format(years[0],years[-1]),mode='a',index=False,header=first)
        count.to_csv("SP-2010-RACACOR.csv",index=False,na_rep='missing')
        if first:
            first = False

