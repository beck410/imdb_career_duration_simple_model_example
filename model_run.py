from build_professional_duration_prediction_dataset import (
    get_final_df_mapping,
    merge_df_datasets
)
from career_duration_test_model import (
    split_dataset,
    build_model,
    test_model
)


def main():
    df_mapping = get_final_df_mapping()
    stage_df = merge_df_datasets(df_mapping)
    features_df = build_features_dataset(stage_df)
    split_datasets = split_dataset(features_df)
    model = build_model(split_datasets['train'])
    test_results = test_model(split_datasets['test'])
    import pdb; pdb.set_trace()

if __name__ == "__main__":
    main()
