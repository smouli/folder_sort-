#!/usr/bin/env python3
"""
Test runner for document classification API
Runs comprehensive tests and generates evaluation reports
"""

import argparse
import sys
import time
from pathlib import Path
import json
from test_framework import DocumentClassificationTester, TEST_TEXTS
from evaluation import ClassificationEvaluator, GroundTruthManager, create_sample_ground_truth

def wait_for_api(base_url: str = "http://localhost:8000", timeout: int = 30):
    """Wait for API to be ready"""
    tester = DocumentClassificationTester(base_url)
    
    print(f"Waiting for API at {base_url}...")
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        if tester.test_api_health():
            print("✅ API is ready!")
            return True
        print("⏳ API not ready, waiting...")
        time.sleep(2)
    
    print("❌ API failed to start within timeout")
    return False

def run_basic_tests(base_url: str = "http://localhost:8000"):
    """Run basic functionality tests"""
    print("\n=== Running Basic Tests ===")
    
    tester = DocumentClassificationTester(base_url)
    
    # Test categories endpoint
    print("Testing categories endpoint...")
    categories_result = tester.test_categories_endpoint()
    print(f"Categories test: {categories_result['status']}")
    
    # Test text classification with known examples
    print("\nTesting text classification...")
    for category, text in TEST_TEXTS.items():
        result = tester.test_text_classification(text, expected_category=category)
        status_emoji = "✅" if result["status"] == "pass" else "❌"
        correct_emoji = "✓" if result.get("correct") else "✗" if result.get("correct") is False else "?"
        print(f"{status_emoji} {category}: {result.get('classification', 'unknown')} {correct_emoji}")
    
    # Test edge cases
    print("\nTesting edge cases...")
    edge_results = tester.test_edge_cases()
    passed_edge = len([r for r in edge_results if r.get("status") == "pass"])
    total_edge = len(edge_results)
    print(f"Edge cases: {passed_edge}/{total_edge} passed")
    
    return tester

def run_file_tests(base_url: str = "http://localhost:8000", test_dir: str = None):
    """Run file upload tests"""
    print("\n=== Running File Tests ===")
    
    if not test_dir or not Path(test_dir).exists():
        print(f"Test directory '{test_dir}' not found. Skipping file tests.")
        return None
    
    tester = DocumentClassificationTester(base_url)
    
    # Load ground truth if available
    ground_truth = GroundTruthManager()
    
    print(f"Testing files in {test_dir}...")
    test_files = list(Path(test_dir).glob("*"))
    
    for file_path in test_files:
        if file_path.is_file():
            # Get expected category from ground truth
            expected = ground_truth.get_ground_truth(file_path.name)
            
            result = tester.test_file_upload(str(file_path), expected_category=expected)
            
            status_emoji = "✅" if result["status"] == "pass" else "❌"
            correct_info = ""
            if result.get("correct") is not None:
                correct_emoji = "✓" if result["correct"] else "✗"
                correct_info = f" {correct_emoji} (expected: {expected})"
            
            print(f"{status_emoji} {file_path.name}: {result.get('classification', 'unknown')}{correct_info}")
    
    return tester

def run_evaluation(tester: DocumentClassificationTester):
    """Run evaluation and generate metrics"""
    print("\n=== Running Evaluation ===")
    
    # Extract results for evaluation
    categories = [
        "Finance", "Legal", "Operations", "HR", "Product",
        "Engineering / Tech", "Sales", "Marketing / Communications", 
        "Customer Success / Support", "Strategy / Corp Dev", 
        "Compliance / Risk", "Other"
    ]
    
    evaluator = ClassificationEvaluator(categories)
    
    # Add results from tests
    for result in tester.test_results:
        if result.get("classification") and result.get("expected"):
            processing_time = result.get("processing_time", 0)
            evaluator.add_prediction(
                predicted=result["classification"],
                actual=result["expected"],
                processing_time=processing_time
            )
    
    if evaluator.predictions:
        # Calculate metrics
        metrics = evaluator.calculate_metrics()
        print(f"\n📊 Evaluation Results:")
        print(f"Accuracy: {metrics['accuracy']:.3f}")
        print(f"Macro F1: {metrics['macro_metrics']['f1_score']:.3f}")
        print(f"Weighted F1: {metrics['weighted_metrics']['f1_score']:.3f}")
        
        if metrics.get('performance'):
            print(f"Avg Processing Time: {metrics['performance']['avg_processing_time']:.2f}s")
        
        # Save detailed report
        evaluator.save_evaluation_report("evaluation_report.json")
        print("\n📝 Detailed evaluation report saved to 'evaluation_report.json'")
        
        # Print classification report
        print("\n📋 Classification Report:")
        print(evaluator.generate_classification_report())
        
        return evaluator
    else:
        print("❌ No predictions with ground truth found for evaluation")
        return None

def generate_summary_report(tester: DocumentClassificationTester, evaluator: ClassificationEvaluator = None):
    """Generate comprehensive summary report"""
    print("\n=== Generating Summary Report ===")
    
    # Basic test statistics
    total_tests = len(tester.test_results)
    passed_tests = len([r for r in tester.test_results if r.get("status") == "pass"])
    failed_tests = len([r for r in tester.test_results if r.get("status") == "fail"])
    error_tests = len([r for r in tester.test_results if r.get("status") == "error"])
    
    # Accuracy statistics
    correct_predictions = len([r for r in tester.test_results if r.get("correct") is True])
    total_predictions = len([r for r in tester.test_results if r.get("correct") is not None])
    accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0
    
    # Performance statistics
    processing_times = [r.get("processing_time", 0) for r in tester.test_results if r.get("processing_time")]
    avg_processing_time = sum(processing_times) / len(processing_times) if processing_times else 0
    
    summary = {
        "test_summary": {
            "total_tests": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "errors": error_tests,
            "pass_rate": passed_tests / total_tests if total_tests > 0 else 0
        },
        "accuracy_summary": {
            "correct_predictions": correct_predictions,
            "total_with_ground_truth": total_predictions,
            "accuracy": accuracy
        },
        "performance_summary": {
            "avg_processing_time": avg_processing_time,
            "total_processing_time": sum(processing_times)
        }
    }
    
    if evaluator:
        metrics = evaluator.calculate_metrics()
        summary["detailed_metrics"] = {
            "macro_f1": metrics['macro_metrics']['f1_score'],
            "weighted_f1": metrics['weighted_metrics']['f1_score'],
            "per_class_f1": {cat: metrics['per_class_metrics'][cat]['f1_score'] 
                           for cat in metrics['per_class_metrics']}
        }
    
    # Save summary
    with open("test_summary.json", 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Print summary
    print(f"\n🎯 Test Summary:")
    print(f"Tests: {passed_tests}/{total_tests} passed ({summary['test_summary']['pass_rate']:.1%})")
    print(f"Accuracy: {correct_predictions}/{total_predictions} correct ({accuracy:.1%})")
    print(f"Avg Processing Time: {avg_processing_time:.2f}s")
    
    if evaluator:
        print(f"Macro F1 Score: {summary['detailed_metrics']['macro_f1']:.3f}")
    
    print("\n📄 Complete summary saved to 'test_summary.json'")
    
    return summary

def main():
    parser = argparse.ArgumentParser(description="Run document classification API tests")
    parser.add_argument("--base-url", default="http://localhost:8000", help="API base URL")
    parser.add_argument("--test-dir", help="Directory containing test files")
    parser.add_argument("--create-sample-data", action="store_true", help="Create sample ground truth data")
    parser.add_argument("--wait-timeout", type=int, default=30, help="Timeout for waiting for API")
    parser.add_argument("--skip-basic", action="store_true", help="Skip basic text tests")
    parser.add_argument("--skip-files", action="store_true", help="Skip file upload tests")
    parser.add_argument("--skip-evaluation", action="store_true", help="Skip evaluation")
    
    args = parser.parse_args()
    
    # Create sample data if requested
    if args.create_sample_data:
        print("Creating sample ground truth data...")
        create_sample_ground_truth()
        print("✅ Sample data created")
        return 0
    
    # Wait for API to be ready
    if not wait_for_api(args.base_url, args.wait_timeout):
        print("❌ API not available. Make sure the server is running.")
        return 1
    
    tester = None
    evaluator = None
    
    try:
        # Run basic tests
        if not args.skip_basic:
            tester = run_basic_tests(args.base_url)
        
        # Run file tests
        if not args.skip_files and args.test_dir:
            file_tester = run_file_tests(args.base_url, args.test_dir)
            if tester and file_tester:
                tester.test_results.extend(file_tester.test_results)
            elif file_tester:
                tester = file_tester
        
        # Run evaluation
        if tester and not args.skip_evaluation:
            evaluator = run_evaluation(tester)
        
        # Generate summary
        if tester:
            generate_summary_report(tester, evaluator)
            
            # Save all test results
            tester.save_results("all_test_results.json")
            print("\n💾 All test results saved to 'all_test_results.json'")
        
        print("\n🎉 Testing completed successfully!")
        return 0
        
    except KeyboardInterrupt:
        print("\n⏹️ Testing interrupted by user")
        return 1
    except Exception as e:
        print(f"\n💥 Testing failed with error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
