
#    _|_
#   /@-@\ Copyright © OpsBeacon, Inc.
#   \ - /    All rights reserved.
#    };{
 
import argparse
import json
import pathlib

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="input file name", type=pathlib.Path)

    args = parser.parse_args()

    if args.input_file:
        try:
            with open(args.input_file, "r") as f:
                data = json.load(f)
                print(data)
        except FileNotFoundError:
            print("File not found")
            return
        except json.decoder.JSONDecodeError:
            print("Invalid JSON file")
            return

if __name__ == "__main__":
    main()
