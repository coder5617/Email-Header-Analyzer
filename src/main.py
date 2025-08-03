#!/usr/bin/env python3
import argparse
from dotenv import load_dotenv
load_dotenv()
from email_header_analyzer.core.parser import EmailHeaderParser

def run_streamlit():
    import subprocess
    subprocess.run([
        "streamlit", "run", "src/email_header_analyzer/ui/streamlit_app.py",
        "--server.port=8501",
        "--server.address=0.0.0.0"
    ])

def main():
    parser = argparse.ArgumentParser(description="Email Header Analyzer")
    parser.add_argument("--mode", choices=["cli","web"], default="web")
    parser.add_argument("--file", help="Header file for CLI analysis")
    parser.add_argument("--header", help="Raw header string for CLI analysis")
    args = parser.parse_args()

    if args.mode == "web":
        run_streamlit()
    else:
        if not (args.file or args.header):
            print("Error: CLI mode requires --file or --header")
            exit(1)
        raw_headers = ""
        if args.file:
            try:
                with open(args.file, "r", encoding="utf-8") as f:
                    raw_headers = f.read()
            except FileNotFoundError:
                print(f"Error: File not found {args.file}")
                exit(1)
        else:
            raw_headers = args.header

        parser = EmailHeaderParser()
        result = parser.analyze_headers(raw_headers)

        print("="*60)
        print("EMAIL HEADER ANALYSIS RESULTS")
        print("="*60)
        for section, data in result.items():
            print(section.upper())
            if isinstance(data, dict):
                for k, v in data.items():
                    print(f"  {k}: {v}")
            else:
                print(data)

if __name__ == "__main__":
    main()
