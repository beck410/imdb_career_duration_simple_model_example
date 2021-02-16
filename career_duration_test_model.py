from sklearn import linear_model

def split_dataset(df, num_rows_train, num_rows_test):
    train_x = stage_df[feature_cols].head(num_rows_train).dropna()
    train_y = stage_df[label_col].head(num_rows_train).dropna()

    test_x = stage_df[feature_cols].tail(num_rows_test).dropna()
    test_y = stage_df[label_col].tail(num_rows_test).dropna()

    return {
        'train': (train_x, train_y),
        'test': (test_x, test_y)
    }

def build_model(train_dataset):
    regr = linear_model.LinearRegression()
    regr.fit(train_dataset[0], train_dataset[1])
    return regr

def test_model(test_dataset):
    test_predictions = regr.predict(test_x[0])
    return((test_predictions, test_predictions[1]))
