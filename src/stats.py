import numpy as np
import pandas as pd

def makeStats(filepath):
    df = pd.read_csv(filepath)

    percent = []
    for i in range(len(df.index)):
        percent.append(
            round((df.iloc[i][2])/(df.iloc[i][1]),5)
            )
    
    df['% Phagocytosis'] = percent 

    df.loc[df.index[0], 'Average Neutrophil Count'] = df['Cell Count'].mean().item()
    df['Average Neutrophil Count'] = df['Average Neutrophil Count'].fillna('')

    df.loc[df.index[0], 'Average % Phagocytosis'] = df['% Phagocytosis'].mean().item()
    df['Average % Phagocytosis'] = df['Average % Phagocytosis'].fillna('')

    df.to_csv(filepath,index=False)

