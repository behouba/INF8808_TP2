'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import pandas as pd
from modes import MODE_TO_COLUMN


def summarize_lines(my_df):
    '''
        Sums each player's total of number of lines and its
        corresponding percentage per act.
    '''

    # On ne garde que les colonnes utiles
    df = my_df[['Act', 'Player']].copy()

    # Compter le nombre de lignes par joueur et par acte
    df = (
        df
        .groupby(['Act', 'Player'])
        .size()
        .reset_index(name='LineCount')
    )

    # Calcul du total de lignes par acte
    total_per_act = df.groupby('Act')['LineCount'].transform('sum')

    # Calcul du pourcentage par joueur dans chaque acte
    df['LinePercent'] = df['LineCount'] / total_per_act * 100

    return df


def replace_others(my_df):
    '''
        Groups players outside the top 5 speakers into 'OTHER'
        for each act.
    '''

    # Identifier les 5 joueurs avec le plus de lignes sur toute la pièce
    top_players = (
        my_df
        .groupby('Player')['LineCount']
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .index
    )

    # Séparer les joueurs du top 5 et les autres
    df_top = my_df[my_df['Player'].isin(top_players)]
    df_other = my_df[~my_df['Player'].isin(top_players)]

    # Regrouper les autres joueurs par acte
    df_other = (
        df_other
        .groupby('Act')
        .agg({
            'LineCount': 'sum',
            'LinePercent': 'sum'
        })
        .reset_index()
    )

    df_other['Player'] = 'OTHER'

    # Combiner les deux
    df_final = pd.concat([df_top, df_other], ignore_index=True)

    return df_final


def clean_names(my_df):
    '''
        Formats player names so each word starts with a capital letter.
    '''

    my_df['Player'] = my_df['Player'].str.title()

    return my_df



if __name__ == "__main__":
    df = pd.read_csv("../assets/data/romeo_and_juliet.csv")

    df = summarize_lines(df)
    df = replace_others(df)
    df = clean_names(df)

    print(df.head(20))
    print("\nColonnes :", df.columns)
