"""Train ML model for ticket classification."""
import pandas as pd
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score


def load_training_data(data_path: str = 'sample_data/synthetic_tickets.csv'):
    """Load training data from CSV.
    
    Args:
        data_path: Path to the training data CSV file
        
    Returns:
        DataFrame with training data
    """
    if not os.path.exists(data_path):
        print(f"Error: Training data file not found at {data_path}")
        print("Please run 'python data/generate_synthetic.py' first to generate synthetic data.")
        return None
    
    df = pd.read_csv(data_path)
    print(f"Loaded {len(df)} tickets from {data_path}")
    return df


def prepare_features(df):
    """Prepare features for training.
    
    Args:
        df: DataFrame with ticket data
        
    Returns:
        Tuple of (X, y) where X is feature matrix and y is target labels
    """
    # Combine title and description for text features
    df['text'] = df['title'] + ' ' + df['description']
    
    X = df['text']
    y = df['category']
    
    return X, y


def train_model(X_train, y_train):
    """Train the classification model.
    
    Args:
        X_train: Training text data
        y_train: Training labels
        
    Returns:
        Tuple of (model, vectorizer)
    """
    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
    
    # Transform training data
    X_train_tfidf = vectorizer.fit_transform(X_train)
    
    # Train Naive Bayes classifier
    model = MultinomialNB()
    model.fit(X_train_tfidf, y_train)
    
    return model, vectorizer


def evaluate_model(model, vectorizer, X_test, y_test):
    """Evaluate the trained model.
    
    Args:
        model: Trained model
        vectorizer: Fitted vectorizer
        X_test: Test text data
        y_test: Test labels
    """
    # Transform test data
    X_test_tfidf = vectorizer.transform(X_test)
    
    # Make predictions
    y_pred = model.predict(X_test_tfidf)
    
    # Print evaluation metrics
    print("\n" + "="*50)
    print("MODEL EVALUATION")
    print("="*50)
    
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nAccuracy: {accuracy:.4f}")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))


def save_model(model, vectorizer, output_path: str = 'models/triage_model.pkl'):
    """Save the trained model to disk.
    
    Args:
        model: Trained model
        vectorizer: Fitted vectorizer
        output_path: Path to save the model
    """
    # Create models directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save model and vectorizer
    with open(output_path, 'wb') as f:
        pickle.dump({
            'model': model,
            'vectorizer': vectorizer
        }, f)
    
    print(f"\nModel saved to {output_path}")


def main():
    """Main training pipeline."""
    print("="*50)
    print("AI TICKET SCHEDULER - MODEL TRAINING")
    print("="*50)
    
    # Load data
    df = load_training_data()
    if df is None:
        return
    
    # Prepare features
    X, y = prepare_features(df)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\nTraining set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")
    
    # Train model
    print("\nTraining model...")
    model, vectorizer = train_model(X_train, y_train)
    
    # Evaluate model
    evaluate_model(model, vectorizer, X_test, y_test)
    
    # Save model
    save_model(model, vectorizer)
    
    print("\n" + "="*50)
    print("Training completed successfully!")
    print("="*50)


if __name__ == '__main__':
    main()
