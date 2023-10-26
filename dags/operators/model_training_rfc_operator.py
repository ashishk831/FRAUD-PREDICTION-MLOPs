from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

class ModelTrainingRFCOperator(BaseOperator):
    """
    Custom Apache Airflow operator to train a machine learning model and save it to a file.
    """
    def __init__(self, X_train_file, y_train_file, model_file, *args, **kwargs):
        """
        Initialize the operator.

        :param X_train_file: File path to the features of the training set (X_train).
        :param y_train_file: File path to the labels of the training set (y_train).
        :param model_file: File path to save the trained model.
        """
        super(ModelTrainingRFCOperator, self).__init__(*args, **kwargs)
        self.X_train_file = X_train_file
        self.y_train_file = y_train_file
        self.model_file = model_file

    def execute(self, context):
        self.log.info(f'Training a machine learning model using data from {self.X_train_file,self.y_train_file }')

        # Retrieve the train data from the previous task using XCom
        #train_data = context['ti'].xcom_pull(task_ids='data_split_task', key='train_data')

        try:
            X_train = pd.read_csv(self.X_train_file)
            y_train = pd.read_csv(self.y_train_file)
            
            print(X_train.shape)
            print(y_train.shape)
            
            # Initialize and train your machine learning model (replace with your model class)
            # model = RandomForestClassifier()  # Replace with your model class and its hyperparameters
            # model.fit(X_train, y_train)
            RFC = RandomForestClassifier(n_estimators=100, random_state=0)
            RFC.fit(X_train, y_train)
            # Save the trained model to the provided model_file
            joblib.dump(RFC, self.model_file)

        except Exception as e:
            self.log.error(f'Model training failed: {str(e)}')
            raise e


