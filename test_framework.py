"""
Comprehensive testing framework for document classification API
Tests different document types, edge cases, and failure modes
"""

import requests
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import pandas as pd
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentClassificationTester:
    """Test framework for document classification API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.test_results = []
        self.categories = [
            "Finance", "Legal", "Operations", "HR", "Product",
            "Engineering / Tech", "Sales", "Marketing / Communications",
            "Customer Success / Support", "Strategy / Corp Dev", 
            "Compliance / Risk", "Other"
        ]
    
    def test_api_health(self) -> bool:
        """Test if API is running and healthy"""
        try:
            response = requests.get(f"{self.base_url}/health")
            return response.status_code == 200
        except:
            return False
    
    def test_categories_endpoint(self) -> Dict:
        """Test categories endpoint"""
        logger.info("Testing categories endpoint...")
        try:
            response = requests.get(f"{self.base_url}/categories")
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "pass",
                    "categories_count": data.get("total_categories", 0),
                    "categories": data.get("categories", [])
                }
            else:
                return {"status": "fail", "error": f"Status code: {response.status_code}"}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def test_text_classification(self, text: str, expected_category: Optional[str] = None) -> Dict:
        """Test text-only classification endpoint"""
        logger.info(f"Testing text classification... (expected: {expected_category})")
        try:
            start_time = time.time()
            response = requests.post(
                f"{self.base_url}/classify",
                json={"text": text}
            )
            end_time = time.time()
            
            if response.status_code == 200:
                data = response.json()
                result = {
                    "status": "pass",
                    "classification": data["results"]["classification"],
                    "summary": data["results"]["summary"],
                    "processing_time": end_time - start_time,
                    "expected": expected_category,
                    "correct": data["results"]["classification"] == expected_category if expected_category else None
                }
            else:
                result = {
                    "status": "fail",
                    "error": f"Status code: {response.status_code}",
                    "response": response.text
                }
            
            self.test_results.append({
                "test_type": "text_classification",
                "timestamp": datetime.now().isoformat(),
                **result
            })
            return result
            
        except Exception as e:
            result = {"status": "error", "error": str(e)}
            self.test_results.append({
                "test_type": "text_classification", 
                "timestamp": datetime.now().isoformat(),
                **result
            })
            return result
    
    def test_file_upload(self, file_path: str, expected_category: Optional[str] = None) -> Dict:
        """Test file upload and classification"""
        logger.info(f"Testing file upload: {file_path} (expected: {expected_category})")
        try:
            start_time = time.time()
            with open(file_path, 'rb') as f:
                files = {'file': (Path(file_path).name, f, 'application/octet-stream')}
                response = requests.post(
                    f"{self.base_url}/upload-and-classify",
                    files=files
                )
            end_time = time.time()
            
            if response.status_code == 200:
                data = response.json()
                result = {
                    "status": "pass",
                    "filename": Path(file_path).name,
                    "classification": data["results"]["classification"],
                    "summary": data["results"]["summary"],
                    "processing_time": end_time - start_time,
                    "parse_time": data["processing"]["parse_time_seconds"],
                    "classify_time": data["processing"]["classify_time_seconds"],
                    "text_length": data["processing"]["text_length"],
                    "expected": expected_category,
                    "correct": data["results"]["classification"] == expected_category if expected_category else None
                }
            else:
                result = {
                    "status": "fail",
                    "filename": Path(file_path).name,
                    "error": f"Status code: {response.status_code}",
                    "response": response.text[:500]  # Truncate long error messages
                }
            
            self.test_results.append({
                "test_type": "file_upload",
                "timestamp": datetime.now().isoformat(),
                **result
            })
            return result
            
        except Exception as e:
            result = {
                "status": "error", 
                "filename": Path(file_path).name,
                "error": str(e)
            }
            self.test_results.append({
                "test_type": "file_upload",
                "timestamp": datetime.now().isoformat(), 
                **result
            })
            return result
    
    def test_edge_cases(self) -> List[Dict]:
        """Test various edge cases"""
        logger.info("Testing edge cases...")
        edge_cases = [
            # Empty inputs
            {"test": "empty_text", "text": "", "should_fail": True},
            {"test": "whitespace_only", "text": "   \n\t   ", "should_fail": True},
            
            # Very short text
            {"test": "single_word", "text": "Invoice", "expected": None},
            {"test": "short_phrase", "text": "Meeting notes", "expected": None},
            
            # Very long text
            {"test": "very_long_text", "text": "This is a contract. " * 1000, "expected": "Legal"},
            
            # Mixed languages/special characters
            {"test": "special_chars", "text": "Contract with émojis 📄 and spëcial chars", "expected": "Legal"},
            
            # Ambiguous content
            {"test": "ambiguous", "text": "Document about something", "expected": "Other"},
            
            # Category boundary cases
            {"test": "finance_legal_mix", "text": "Legal contract for financial services payment terms", "expected": None}
        ]
        
        results = []
        for case in edge_cases:
            if case["test"] in ["empty_text", "whitespace_only"]:
                # These should fail gracefully
                try:
                    response = requests.post(f"{self.base_url}/classify", json={"text": case["text"]})
                    if response.status_code == 400:  # Expected failure
                        results.append({"test": case["test"], "status": "pass", "note": "Failed as expected"})
                    else:
                        results.append({"test": case["test"], "status": "unexpected_success"})
                except:
                    results.append({"test": case["test"], "status": "error"})
            else:
                result = self.test_text_classification(case["text"], case.get("expected"))
                result["test_name"] = case["test"]
                results.append(result)
        
        return results
    
    def test_unsupported_files(self) -> List[Dict]:
        """Test handling of unsupported file types"""
        logger.info("Testing unsupported file types...")
        
        # Create dummy files for testing
        test_files = [
            ("test.xyz", b"dummy content", "application/unknown"),
            ("test.exe", b"dummy exe", "application/x-executable"),
        ]
        
        results = []
        for filename, content, content_type in test_files:
            try:
                files = {'file': (filename, content, content_type)}
                response = requests.post(f"{self.base_url}/upload-and-classify", files=files)
                
                if response.status_code == 400:  # Expected rejection
                    results.append({"filename": filename, "status": "pass", "note": "Rejected as expected"})
                else:
                    results.append({"filename": filename, "status": "unexpected_acceptance"})
            except Exception as e:
                results.append({"filename": filename, "status": "error", "error": str(e)})
        
        return results
    
    def run_comprehensive_tests(self, test_files_dir: Optional[str] = None) -> Dict:
        """Run all tests and return comprehensive results"""
        logger.info("Starting comprehensive test suite...")
        
        # Check API health
        if not self.test_api_health():
            return {"error": "API is not healthy or not running"}
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "api_health": "pass",
            "categories_test": self.test_categories_endpoint(),
            "edge_cases": self.test_edge_cases(),
            "unsupported_files": self.test_unsupported_files(),
            "file_tests": [],
            "summary": {}
        }
        
        # Test files if directory provided
        if test_files_dir and Path(test_files_dir).exists():
            logger.info(f"Testing files in {test_files_dir}")
            for file_path in Path(test_files_dir).glob("*"):
                if file_path.is_file():
                    result = self.test_file_upload(str(file_path))
                    results["file_tests"].append(result)
        
        # Generate summary
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r.get("status") == "pass"])
        failed_tests = len([r for r in self.test_results if r.get("status") == "fail"])
        error_tests = len([r for r in self.test_results if r.get("status") == "error"])
        
        results["summary"] = {
            "total_tests": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "errors": error_tests,
            "pass_rate": passed_tests / total_tests if total_tests > 0 else 0
        }
        
        return results
    
    def save_results(self, filename: str = "test_results.json"):
        """Save test results to file"""
        with open(filename, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        logger.info(f"Test results saved to {filename}")
    
    def generate_report(self) -> str:
        """Generate a human-readable test report"""
        if not self.test_results:
            return "No test results available"
        
        total = len(self.test_results)
        passed = len([r for r in self.test_results if r.get("status") == "pass"])
        failed = len([r for r in self.test_results if r.get("status") == "fail"])
        errors = len([r for r in self.test_results if r.get("status") == "error"])
        
        report = f"""
=== Document Classification API Test Report ===
Generated: {datetime.now().isoformat()}

SUMMARY:
- Total Tests: {total}
- Passed: {passed} ({passed/total*100:.1f}%)
- Failed: {failed} ({failed/total*100:.1f}%)
- Errors: {errors} ({errors/total*100:.1f}%)

DETAILS:
"""
        
        for result in self.test_results:
            status_emoji = {"pass": "✅", "fail": "❌", "error": "⚠️"}.get(result.get("status"), "❓")
            report += f"{status_emoji} {result.get('test_type', 'unknown')}"
            
            if result.get("filename"):
                report += f" - {result['filename']}"
            if result.get("classification"):
                report += f" → {result['classification']}"
            if result.get("correct") is not None:
                report += f" (Expected: {result.get('expected')}) {'✓' if result['correct'] else '✗'}"
            if result.get("error"):
                report += f" - ERROR: {result['error']}"
            
            report += "\n"
        
        return report


# Sample usage and test data
TEST_TEXTS = {
    "Finance": "Q3 Budget Report: Revenue increased 15% to $2.5M. Operating expenses $1.8M. Net profit $700K.",
    "Legal": "Master Services Agreement between TechCorp Inc. and ServiceProvider LLC. Term: 24 months. Payment: $50,000 monthly.",
    "HR": "Employee Handbook: PTO Policy. Full-time employees accrue 15 days annually. Sick leave: 10 days.",
    "Sales": "Sales Pipeline Report: 15 qualified leads, $500K potential revenue. Close rate: 25%.",
    "Other": "Random notes about weekend plans and grocery shopping list."
}

if __name__ == "__main__":
    # Example usage
    tester = DocumentClassificationTester()
    
    # Test with sample texts
    for category, text in TEST_TEXTS.items():
        tester.test_text_classification(text, expected_category=category)
    
    # Run comprehensive tests
    results = tester.run_comprehensive_tests()
    
    # Generate and print report
    report = tester.generate_report()
    print(report)
    
    # Save results
    tester.save_results()
