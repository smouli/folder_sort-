"""
Evaluation framework for document classification accuracy and performance
Includes metrics, confusion matrix, and performance benchmarking
"""

import json
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class ClassificationEvaluator:
    """Evaluate classification performance and generate metrics"""
    
    def __init__(self, categories: List[str]):
        self.categories = categories
        self.predictions = []
        self.ground_truth = []
        self.processing_times = []
        self.confidence_scores = []
    
    def add_prediction(self, predicted: str, actual: str, processing_time: float = None, confidence: float = None):
        """Add a prediction result for evaluation"""
        self.predictions.append(predicted)
        self.ground_truth.append(actual)
        if processing_time:
            self.processing_times.append(processing_time)
        if confidence:
            self.confidence_scores.append(confidence)
    
    def calculate_metrics(self) -> Dict:
        """Calculate comprehensive classification metrics"""
        if not self.predictions or not self.ground_truth:
            return {"error": "No predictions to evaluate"}
        
        # Basic accuracy
        accuracy = accuracy_score(self.ground_truth, self.predictions)
        
        # Per-class metrics
        precision, recall, f1, support = precision_recall_fscore_support(
            self.ground_truth, self.predictions, labels=self.categories, average=None, zero_division=0
        )
        
        # Macro and weighted averages
        macro_precision, macro_recall, macro_f1, _ = precision_recall_fscore_support(
            self.ground_truth, self.predictions, average='macro', zero_division=0
        )
        
        weighted_precision, weighted_recall, weighted_f1, _ = precision_recall_fscore_support(
            self.ground_truth, self.predictions, average='weighted', zero_division=0
        )
        
        # Confusion matrix
        cm = confusion_matrix(self.ground_truth, self.predictions, labels=self.categories)
        
        # Performance metrics
        performance_metrics = {}
        if self.processing_times:
            performance_metrics = {
                "avg_processing_time": np.mean(self.processing_times),
                "median_processing_time": np.median(self.processing_times),
                "min_processing_time": np.min(self.processing_times),
                "max_processing_time": np.max(self.processing_times)
            }
        
        return {
            "timestamp": datetime.now().isoformat(),
            "total_samples": len(self.predictions),
            "accuracy": accuracy,
            "macro_metrics": {
                "precision": macro_precision,
                "recall": macro_recall,
                "f1_score": macro_f1
            },
            "weighted_metrics": {
                "precision": weighted_precision,
                "recall": weighted_recall,
                "f1_score": weighted_f1
            },
            "per_class_metrics": {
                category: {
                    "precision": precision[i],
                    "recall": recall[i],
                    "f1_score": f1[i],
                    "support": int(support[i])
                }
                for i, category in enumerate(self.categories)
            },
            "confusion_matrix": cm.tolist(),
            "performance": performance_metrics
        }
    
    def generate_classification_report(self) -> str:
        """Generate detailed classification report"""
        if not self.predictions or not self.ground_truth:
            return "No predictions to evaluate"
        
        return classification_report(
            self.ground_truth, 
            self.predictions, 
            labels=self.categories,
            target_names=self.categories,
            zero_division=0
        )
    
    def plot_confusion_matrix(self, save_path: Optional[str] = None, figsize: Tuple[int, int] = (12, 10)):
        """Plot confusion matrix heatmap"""
        if not self.predictions or not self.ground_truth:
            logger.error("No predictions to plot")
            return
        
        cm = confusion_matrix(self.ground_truth, self.predictions, labels=self.categories)
        
        plt.figure(figsize=figsize)
        sns.heatmap(
            cm, 
            annot=True, 
            fmt='d', 
            cmap='Blues',
            xticklabels=self.categories,
            yticklabels=self.categories
        )
        plt.title('Document Classification Confusion Matrix')
        plt.xlabel('Predicted Category')
        plt.ylabel('True Category')
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Confusion matrix saved to {save_path}")
        
        plt.show()
    
    def analyze_errors(self) -> Dict:
        """Analyze misclassification patterns"""
        if not self.predictions or not self.ground_truth:
            return {"error": "No predictions to analyze"}
        
        errors = []
        for i, (pred, true) in enumerate(zip(self.predictions, self.ground_truth)):
            if pred != true:
                errors.append({
                    "index": i,
                    "predicted": pred,
                    "actual": true,
                    "processing_time": self.processing_times[i] if i < len(self.processing_times) else None
                })
        
        # Common error patterns
        error_patterns = {}
        for error in errors:
            pattern = f"{error['actual']} → {error['predicted']}"
            error_patterns[pattern] = error_patterns.get(pattern, 0) + 1
        
        # Sort by frequency
        sorted_patterns = sorted(error_patterns.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "total_errors": len(errors),
            "error_rate": len(errors) / len(self.predictions),
            "error_patterns": dict(sorted_patterns[:10]),  # Top 10 patterns
            "detailed_errors": errors[:20]  # First 20 detailed errors
        }
    
    def performance_benchmarks(self) -> Dict:
        """Calculate performance benchmarks"""
        metrics = {}
        
        if self.processing_times:
            times = np.array(self.processing_times)
            metrics["processing_time"] = {
                "mean": float(np.mean(times)),
                "median": float(np.median(times)),
                "std": float(np.std(times)),
                "p95": float(np.percentile(times, 95)),
                "p99": float(np.percentile(times, 99)),
                "throughput_per_second": 1.0 / np.mean(times) if np.mean(times) > 0 else 0
            }
        
        # Calculate accuracy by category
        accuracy_by_category = {}
        for category in self.categories:
            category_indices = [i for i, true_cat in enumerate(self.ground_truth) if true_cat == category]
            if category_indices:
                category_predictions = [self.predictions[i] for i in category_indices]
                category_actual = [self.ground_truth[i] for i in category_indices]
                accuracy_by_category[category] = accuracy_score(category_actual, category_predictions)
        
        metrics["accuracy_by_category"] = accuracy_by_category
        
        return metrics
    
    def save_evaluation_report(self, filepath: str):
        """Save comprehensive evaluation report"""
        report = {
            "evaluation_metadata": {
                "timestamp": datetime.now().isoformat(),
                "total_predictions": len(self.predictions),
                "categories": self.categories
            },
            "metrics": self.calculate_metrics(),
            "error_analysis": self.analyze_errors(),
            "performance_benchmarks": self.performance_benchmarks(),
            "classification_report": self.generate_classification_report()
        }
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Evaluation report saved to {filepath}")
        return report


class GroundTruthManager:
    """Manage ground truth data for evaluation"""
    
    def __init__(self, ground_truth_file: str = "ground_truth.json"):
        self.ground_truth_file = ground_truth_file
        self.ground_truth = self.load_ground_truth()
    
    def load_ground_truth(self) -> Dict:
        """Load ground truth labels from file"""
        if Path(self.ground_truth_file).exists():
            with open(self.ground_truth_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_ground_truth(self):
        """Save ground truth labels to file"""
        with open(self.ground_truth_file, 'w') as f:
            json.dump(self.ground_truth, f, indent=2)
    
    def add_ground_truth(self, document_id: str, true_category: str, document_info: Dict = None):
        """Add ground truth label for a document"""
        self.ground_truth[document_id] = {
            "category": true_category,
            "timestamp": datetime.now().isoformat(),
            "document_info": document_info or {}
        }
        self.save_ground_truth()
    
    def get_ground_truth(self, document_id: str) -> Optional[str]:
        """Get ground truth label for a document"""
        return self.ground_truth.get(document_id, {}).get("category")
    
    def create_test_dataset(self) -> Dict:
        """Create structured test dataset from ground truth"""
        test_data = {
            "metadata": {
                "created": datetime.now().isoformat(),
                "total_documents": len(self.ground_truth),
                "categories": {}
            },
            "documents": []
        }
        
        # Count documents per category
        category_counts = {}
        for doc_id, data in self.ground_truth.items():
            category = data["category"]
            category_counts[category] = category_counts.get(category, 0) + 1
            
            test_data["documents"].append({
                "document_id": doc_id,
                "true_category": category,
                "timestamp": data.get("timestamp"),
                "document_info": data.get("document_info", {})
            })
        
        test_data["metadata"]["categories"] = category_counts
        return test_data


# Utility functions for creating test datasets
def create_sample_ground_truth():
    """Create sample ground truth data for testing"""
    sample_data = {
        "invoice_001.pdf": {
            "category": "Finance",
            "timestamp": datetime.now().isoformat(),
            "document_info": {"type": "invoice", "amount": "$5000"}
        },
        "contract_msa.pdf": {
            "category": "Legal", 
            "timestamp": datetime.now().isoformat(),
            "document_info": {"type": "contract", "parties": "TechCorp, ServiceProvider"}
        },
        "employee_handbook.pdf": {
            "category": "HR",
            "timestamp": datetime.now().isoformat(),
            "document_info": {"type": "handbook", "pages": 50}
        },
        "sales_report_q3.pdf": {
            "category": "Sales",
            "timestamp": datetime.now().isoformat(),
            "document_info": {"type": "report", "period": "Q3 2024"}
        },
        "product_roadmap.pdf": {
            "category": "Product",
            "timestamp": datetime.now().isoformat(),
            "document_info": {"type": "roadmap", "version": "2024"}
        }
    }
    
    with open("sample_ground_truth.json", 'w') as f:
        json.dump(sample_data, f, indent=2)
    
    return sample_data


if __name__ == "__main__":
    # Example usage
    categories = [
        "Finance", "Legal", "Operations", "HR", "Product",
        "Engineering / Tech", "Sales", "Marketing / Communications", 
        "Customer Success / Support", "Strategy / Corp Dev", 
        "Compliance / Risk", "Other"
    ]
    
    # Create evaluator
    evaluator = ClassificationEvaluator(categories)
    
    # Simulate some predictions for testing
    test_predictions = [
        ("Finance", "Finance", 2.5),
        ("Legal", "Legal", 3.1),
        ("HR", "Finance", 2.8),  # Misclassification
        ("Sales", "Sales", 1.9),
        ("Other", "Product", 2.2),  # Misclassification
    ]
    
    for pred, actual, time_taken in test_predictions:
        evaluator.add_prediction(pred, actual, time_taken)
    
    # Calculate metrics
    metrics = evaluator.calculate_metrics()
    print("Classification Metrics:")
    print(json.dumps(metrics, indent=2))
    
    # Generate report
    report = evaluator.generate_classification_report()
    print("\nDetailed Classification Report:")
    print(report)
    
    # Analyze errors
    errors = evaluator.analyze_errors()
    print("\nError Analysis:")
    print(json.dumps(errors, indent=2))
    
    # Create sample ground truth
    create_sample_ground_truth()
    print("\nSample ground truth created in 'sample_ground_truth.json'")
