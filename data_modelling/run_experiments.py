import click
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from skopt import BayesSearchCV
from model_dict import MODELS_DICT, MODELS_PARAMS


@click.command()
@click.option('--model_names_list', required=True, type=str, help='list of models to run')
@click.option('--n_iter', required=True, type=int, help='number of iterations for hyperparameters tuning')
def main(model_names_list, n_iter):
    """
    Runs experiments with BayesSearch for selected models using the specified dataset

    Usage:
    ```
    python run_experiments.py --model_names_list=Lasso,DT,RF,SVR,LGB,GBM,XGB --n_iter=10
    ```
    """
    print('Loading models...')
    model_dict = {}

    dataset = 'model_data.csv'

    try:
        df = pd.read_csv(dataset)
        x = df.drop('price', axis=1)
        y = df['price']

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

        for model_name in model_names_list.split(','):
            assert model_name in MODELS_DICT.keys(), f'Unknown model_name: {model_name}'
            model = MODELS_DICT[model_name]
            model_dict[model_name] = model

        for model_name, model in model_dict.items():
            print(f'Running experiments for {model_name}')
            pipe = Pipeline([('scaler', StandardScaler()), ('regressor_model', model)])
            opt = BayesSearchCV(
                pipe,
                MODELS_PARAMS[model_name],
                n_iter=n_iter,
                random_state=7,
                verbose=True
            )
            opt.fit(x_train, y_train)

            best_score = opt.score(x_test, y_test)
            best_params = opt.best_params_

            result_df = pd.DataFrame([{**{'Model': model_name, 'Score': best_score}, **best_params}])
            result_df.to_csv(f'reports/model_results_{model_name}.csv', index=False)

    except Exception as e:
        print(f'An error occurred: {e}')


if __name__ == '__main__':
    main()
