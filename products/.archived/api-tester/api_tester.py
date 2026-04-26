#!/usr/bin/env python3
"""
API Tester CLI - Professional API testing and validation tool
Part of the UniverseCreator Developer Toolkit
"""

import argparse
import json
import sys
import time
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Optional, Any


class APITester:
    """Professional API testing tool with comprehensive validation."""

    def __init__(self):
        self.results = []
        self.session = None

    def test_endpoint(self, url: str, method: str = "GET", headers: Dict = None,
                     data: Any = None, expected_status: int = 200,
                     timeout: int = 30) -> Dict:
        """Test a single API endpoint."""
        import requests

        start_time = time.time()
        result = {
            "url": url,
            "method": method,
            "status": None,
            "response_time": None,
            "success": False,
            "error": None,
            "headers_sent": headers or {},
            "headers_received": {},
            "body_preview": None
        }

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=data if data else None,
                timeout=timeout
            )

            result["status"] = response.status_code
            result["response_time"] = round((time.time() - start_time) * 1000, 2)
            result["headers_received"] = dict(response.headers)
            result["success"] = response.status_code == expected_status

            # Body preview (first 500 chars)
            try:
                body = response.text[:500]
                result["body_preview"] = body
            except:
                result["body_preview"] = "<binary content>"

        except requests.exceptions.Timeout:
            result["error"] = f"Timeout after {timeout}s"
        except requests.exceptions.ConnectionError:
            result["error"] = "Connection failed"
        except Exception as e:
            result["error"] = str(e)

        return result

    def run_collection(self, collection: List[Dict]) -> List[Dict]:
        """Run a collection of API tests."""
        results = []
        for test in collection:
            result = self.test_endpoint(
                url=test.get("url"),
                method=test.get("method", "GET"),
                headers=test.get("headers"),
                data=test.get("data"),
                expected_status=test.get("expected_status", 200),
                timeout=test.get("timeout", 30)
            )
            results.append(result)
        return results

    def generate_report(self, results: List[Dict]) -> str:
        """Generate a formatted test report."""
        total = len(results)
        passed = sum(1 for r in results if r["success"])
        failed = total - passed

        report = []
        report.append("=" * 60)
        report.append("API TEST REPORT")
        report.append("=" * 60)
        report.append(f"Total Tests: {total}")
        report.append(f"Passed: {passed} ✅")
        report.append(f"Failed: {failed} ❌")
        report.append(f"Success Rate: {(passed/total*100):.1f}%")
        report.append("=" * 60)
        report.append("")

        for i, result in enumerate(results, 1):
            status = "✅ PASS" if result["success"] else "❌ FAIL"
            report.append(f"Test {i}: {status}")
            report.append(f"  URL: {result['method']} {result['url']}")
            report.append(f"  Status: {result['status']}")
            if result['response_time']:
                report.append(f"  Response Time: {result['response_time']}ms")
            if result['error']:
                report.append(f"  Error: {result['error']}")
            report.append("")

        return "\n".join(report)


def interactive_mode():
    """Interactive mode for guided API testing."""
    print("🌐 API Tester - Interactive Mode")
    print("=" * 50)

    tester = APITester()

    url = input("Enter API URL: ").strip()
    if not url:
        print("❌ URL is required")
        return

    print("\nSelect HTTP method:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]
    for i, method in enumerate(methods, 1):
        print(f"  {i}. {method}")

    try:
        method_choice = int(input("\nChoice (1-7): "))
        method = methods[method_choice - 1]
    except (ValueError, IndexError):
        method = "GET"
        print(f"Using default: {method}")

    # Headers
    headers = {}
    if input("\nAdd custom headers? (y/n): ").lower() == 'y':
        print("Enter headers (blank line to finish):")
        while True:
            header_line = input("Header (Key: Value): ").strip()
            if not header_line:
                break
            if ':' in header_line:
                key, value = header_line.split(':', 1)
                headers[key.strip()] = value.strip()

    # Request body
    data = None
    if method in ["POST", "PUT", "PATCH"]:
        if input("\nAdd request body? (y/n): ").lower() == 'y':
            print("Enter JSON body:")
            try:
                body_input = input()
                data = json.loads(body_input)
            except json.JSONDecodeError:
                print("⚠️ Invalid JSON, proceeding without body")

    # Expected status
    expected_status = 200
    try:
        expected_input = input(f"\nExpected status code [{expected_status}]: ").strip()
        if expected_input:
            expected_status = int(expected_input)
    except ValueError:
        pass

    print(f"\n🚀 Running test...")
    result = tester.test_endpoint(url, method, headers, data, expected_status)

    print("\n" + tester.generate_report([result]))


def main():
    parser = argparse.ArgumentParser(
        description="API Tester CLI - Professional API testing tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  api-tester --interactive              # Interactive mode
  api-tester https://api.example.com    # Quick GET test
  api-tester https://api.example.com --method POST --data '{"key":"value"}'
  api-tester --collection tests.json    # Run test collection
        """
    )

    parser.add_argument("url", nargs="?", help="API endpoint URL to test")
    parser.add_argument("-i", "--interactive", action="store_true",
                       help="Run in interactive mode")
    parser.add_argument("-m", "--method", default="GET",
                       choices=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"],
                       help="HTTP method (default: GET)")
    parser.add_argument("-d", "--data", help="Request body (JSON string)")
    parser.add_argument("-H", "--header", action="append", dest="headers",
                       help="Custom header (can be used multiple times)")
    parser.add_argument("-e", "--expected", type=int, default=200,
                       help="Expected status code (default: 200)")
    parser.add_argument("-t", "--timeout", type=int, default=30,
                       help="Request timeout in seconds (default: 30)")
    parser.add_argument("-c", "--collection", help="Run test collection from JSON file")
    parser.add_argument("-o", "--output", help="Save results to file")
    parser.add_argument("--format", choices=["text", "json"], default="text",
                       help="Output format (default: text)")

    args = parser.parse_args()

    tester = APITester()

    # Interactive mode
    if args.interactive or (not args.url and not args.collection):
        interactive_mode()
        return

    # Collection mode
    if args.collection:
        try:
            with open(args.collection, 'r') as f:
                collection = json.load(f)
            results = tester.run_collection(collection)
        except FileNotFoundError:
            print(f"❌ Collection file not found: {args.collection}")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON in collection file")
            sys.exit(1)
    else:
        # Single test mode
        headers = {}
        if args.headers:
            for header in args.headers:
                if ':' in header:
                    key, value = header.split(':', 1)
                    headers[key.strip()] = value.strip()

        data = None
        if args.data:
            try:
                data = json.loads(args.data)
            except json.JSONDecodeError:
                print("❌ Invalid JSON in data")
                sys.exit(1)

        result = tester.test_endpoint(
            args.url, args.method, headers, data, args.expected, args.timeout
        )
        results = [result]

    # Generate output
    if args.format == "json":
        output = json.dumps(results, indent=2)
    else:
        output = tester.generate_report(results)

    # Output results
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"✅ Results saved to {args.output}")
    else:
        print(output)

    # Exit with appropriate code
    failed = sum(1 for r in results if not r["success"])
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
