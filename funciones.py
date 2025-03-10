def cargar_excel_csv(archivo):
    import pandas as pd
    import os
    extension = os.path.splitext(archivo)[1].lower()
    if extension == '.csv':
        df = pd.read_csv(archivo)
        df = df.drop(df.columns[0], axis=1)
        return(df)
    elif extension == '.xlsx':
        df = pd.read_excel(archivo)
        df = df.drop(df.columns[0], axis=1)
        return(df)
    else:
            raise ValueError('Este formato no está soportado para esta función:',extension)

def sustitucion_nulos(df):
    import pandas as pd
    import numpy as np
    cuantitativas = df.select_dtypes(include=['float64', 'int64','float','int'])
    cualitativas = df.select_dtypes(include=['object', 'datetime','category'])
    columnas = np.arange(len(cuantitativas.columns))
    
    pares = cuantitativas.iloc[:,columnas%2==0].fillna(cuantitativas.mean().round(1))
    impares = cuantitativas.iloc[:,columnas%2!=0].fillna(99)

    cualitativas_rellenas = cualitativas.fillna('Este_es_un_valor_nulo')

    df = pd.concat([pares,impares,cualitativas_rellenas],axis=1)

    return(df)
     
def contar_nulos(df):
    import pandas as pd
    import numpy as np

    nulos_por_columna = df.isnull().sum()
    nulos_totales = df.isnull().sum().sum()
    return ('Nulos por columna:',nulos_por_columna,'Nulos totales:',nulos_totales)

def sustituir_atipicos(df):
    import pandas as pd
    import numpy as np    
    
    cualitativas = df.select_dtypes(include=['object', 'datetime','category'])
    cuantitativas = df.select_dtypes(include=['float64', 'int64','float','int'])

    y = cuantitativas

    percentile25 = y.quantile(0.25)#Q1
    percentile75 = y.quantile(0.75)#Q3
    iqr = percentile75-percentile25

    limite_superior_iqr = percentile75+1.5*iqr
    limite_inferior_iqr = percentile25-1.5*iqr
    print('Limite superior permitido',limite_superior_iqr)
    print('Limite inferior permitido',limite_inferior_iqr)

    df_iqr = cuantitativas[(y<=limite_superior_iqr)&(y>=limite_inferior_iqr)]
    df_final_iqr = df_iqr.fillna(round(df_iqr.mean(),1))
    return(pd.concat([cualitativas,df_final_iqr],axis=1))
