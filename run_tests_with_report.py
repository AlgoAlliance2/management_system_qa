import pytest
import os
import sys
from datetime import datetime

def run_tests():
    """
    Runs pytest and saves the output to a timestamped file in test_reports/
    Also generates an HTML report.
    """
    # Create reports directory if not exists
    reports_dir = os.path.join(os.path.dirname(__file__), "test_reports")
    os.makedirs(reports_dir, exist_ok=True)

    # Generate timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Define report filenames
    html_report = os.path.join(reports_dir, f"report_{timestamp}.html")
    log_file = os.path.join(reports_dir, f"output_{timestamp}.txt")
    
    # Arguments for pytest
    # --html for HTML report
    # --capture=tee-sys to see output in console AND capture it (standard logging setup might be needed for file)
    # But pytest-html handles the visual report. 
    # To save console output to txt, we can't easily do it via pytest args while also showing it, 
    # unless we use tee or similar. 
    # Simpler: We will run pytest and rely on the HTML report for detailed analysis, 
    # and maybe redirect stdout to a file if the user runs this script manually.
    
    print(f"🚀 Running tests... Reports will be saved to: {reports_dir}")
    print(f"📄 HTML Report: {os.path.basename(html_report)}")
    
    # Build arguments
    # We pass the arguments to pytest.main()
    args = [
        "--html=" + html_report,
        "--self-contained-html",
        "-v"
    ]
    
    # Allow passing extra args from command line (e.g., specific test file)
    args.extend(sys.argv[1:])
    
    # Run pytest
    result = pytest.main(args)
    
    print(f"\n✅ Test run complete. Exit code: {result}")
    print(f"📂 View report: {html_report}")
    
    return result

if __name__ == "__main__":
    sys.exit(run_tests())
