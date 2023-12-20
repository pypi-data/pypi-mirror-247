def explain_df(df):
    summary_data = []

    for column in df.columns:
        data_type = df[column].dtype
        unique_values = df[column].nunique()
        null_values = df[column].isnull().sum()
        summary_data.append([column, data_type, unique_values, null_values])


    summary_df = pd.DataFrame(summary_data, columns=['Column', 'Data Type', 'Unique Values','Null Values'])
    return summary_df