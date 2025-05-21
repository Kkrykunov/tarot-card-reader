"""
Test runner for the Tarot Card Reading Application.

Run all tests and generate a comprehensive test report.
"""

import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def run_all_tests():
    """Run all tests and return the result."""
    # Discover and run all tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result

def main():
    """Main entry point for test runner."""
    print("=" * 60)
    print("Tarot Card Reading Application - Test Suite")
    print("=" * 60)
    
    result = run_all_tests()
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.failures:
        print("\nFailures:")
        for test, trace in result.failures:
            print(f"- {test}: {trace.splitlines()[-1]}")
    
    if result.errors:
        print("\nErrors:")
        for test, trace in result.errors:
            print(f"- {test}: {trace.splitlines()[-1]}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    print(f"\nOverall result: {'PASSED' if success else 'FAILED'}")
    print("=" * 60)
    
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())