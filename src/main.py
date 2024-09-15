import os
import re
import pandas as pd
from xgboost import XGBRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from concurrent.futures import ProcessPoolExecutor
import joblib
from preprocessing import preprocess_all_images  # Assuming these are implemented
from ocr_extraction import extract_text_from_images
from parse_entity import parse_entities

# Define paths
DATASET_FOLDER = './dataset/'
TRAIN_CSV = os.path.join(DATASET_FOLDER, 'train.csv')
TEST_CSV = os.path.join(DATASET_FOLDER, 'test.csv')
OCR_OUTPUT_FILE = 'ocr_output.csv'
TEST_OUT_FILE = 'test.out'


def preprocess_data_concurrently():
    """Preprocess and extract text from images using concurrency for efficiency."""
    preprocess_all_images()
    
    # Concurrently process OCR extraction
    with ProcessPoolExecutor() as executor:
        image_files = os.listdir('preprocessed_images')
        futures = [executor.submit(extract_text_from_images, f) for f in image_files]
        
        # Wait for all tasks to complete
        for future in futures:
            future.result()


def load_data():
    """Load OCR extracted text and parse entities."""
    ocr_data = pd.read_csv(OCR_OUTPUT_FILE, encoding='ISO-8859-1')

    # Convert OCR output to dictionary
    text_data = ocr_data.set_index('image_file')['extracted_text'].to_dict()

    # Parse entities from text data
    parsed_data = parse_entities(text_data)

    return parsed_data


def split_value_and_unit(entity_value):
    """Efficiently extract numeric value and unit using optimized regex."""
    numeric_part = re.search(r"[-+]?\d*\.\d+|\d+", entity_value)
    unit_part = re.search(r'[a-zA-Z]+', entity_value)
    
    value = numeric_part.group() if numeric_part else None
    unit = unit_part.group().lower() if unit_part else None  # Normalize unit to lowercase
    return value, unit


def prepare_datasets(parsed_data):
    """Prepare training and test datasets."""
    # Load training and test data
    train_data = pd.read_csv(TRAIN_CSV)
    test_data = pd.read_csv(TEST_CSV)

    # Vectorized entity extraction
    train_data[['value', 'unit']] = train_data['entity_value'].apply(
        lambda x: pd.Series(split_value_and_unit(x))
    )

    # Handle potential conversion issues
    train_data['value'] = pd.to_numeric(train_data['value'], errors='coerce')
    train_data = train_data.dropna(subset=['value'])
    
    # Prepare training features and labels
    X_train = train_data[['entity_name']]  # Categorical feature
    y_train = train_data['value'].astype(float)  # Numeric value for regression
    
    # Prepare test features
    X_test = test_data[['entity_name']]  # Categorical feature
    test_units = test_data['entity_name'].apply(lambda x: split_value_and_unit(x)[1])  # Units for later use

    return X_train, y_train, X_test, test_units, test_data


def encode_features(X_train, X_test):
    """Apply one-hot encoding to categorical features with memory efficiency."""
    column_transformer = ColumnTransformer(transformers=[
        ('entity_name', OneHotEncoder(handle_unknown='ignore'), ['entity_name'])
    ])
    
    # Apply the transformation to training and test data
    X_train_encoded = column_transformer.fit_transform(X_train)
    X_test_encoded = column_transformer.transform(X_test)
    
    # Save the column transformer for future use
    joblib.dump(column_transformer, 'column_transformer.pkl')
    
    return X_train_encoded, X_test_encoded


def train_model(X_train, y_train):
    """Train an XGBRegressor for numeric value prediction."""
    model = XGBRegressor(objective='reg:squarederror', n_estimators=500, max_depth=6, learning_rate=0.05)
    
    # Create pipeline with imputation in case of missing values
    pipeline = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='mean')),  # Impute missing values
        ('regressor', model)
    ])
    
    # Fit the model to training data
    pipeline.fit(X_train, y_train)
    
    # Save the trained model
    joblib.dump(pipeline, 'model.pkl')
    print("Model saved as 'model.pkl'")
    
    return pipeline


def predict_and_save(model, X_test, test_units, test_data):
    """Make predictions and save results to a file in the required format."""
    predictions = model.predict(X_test)
    
    # Combine predictions with units
    predicted_values_with_units = [
        f"{pred:.2f} {unit}" if unit else f"{pred:.2f}"
        for pred, unit in zip(predictions, test_units)
    ]
    
    # Create the output DataFrame with 'index' and 'entity_value'
    output_df = pd.DataFrame({
        'index': test_data['index'],
        'entity_value': predicted_values_with_units
    })
    
    # Save predictions to test.out
    output_df.to_csv(TEST_OUT_FILE, index=False)
    print(f"Predictions saved to {TEST_OUT_FILE}")


def main():
    """Main function to execute the workflow."""
    try:
        preprocess_data_concurrently()  # Preprocess and extract text concurrently
        parsed_data = load_data()  # Load OCR data and parse entities
        X_train, y_train, X_test, test_units, test_data = prepare_datasets(parsed_data)  # Prepare datasets
        
        # Encode features
        X_train_encoded, X_test_encoded = encode_features(X_train, X_test)
        
        # Train model
        model = train_model(X_train_encoded, y_train)
        
        # Predict and save results for test data
        predict_and_save(model, X_test_encoded, test_units, test_data)

    except Exception as e:
        print(f"An error occurred: {e}")


if _name_ == '_main_':
    main()