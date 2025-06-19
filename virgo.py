import sys 
from virgo.core.lightserver import serve

if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else ""

    if command == "lightserve":
        serve()
    else:
        print("Unknown command. Try: py virgo.py lightserve")