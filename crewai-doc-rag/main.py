from DocRagCrew import DocRagCrew
import logging, os
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def run_main():
    print("Running main")

    file_path = os.path.join(os.path.dirname(__file__), 'input.txt')
    try:
        with open(file_path, 'r') as f:
            input_text = f.read()
    except FileNotFoundError:
        print(f"Error: Could not find {file_path}")
        exit(1)

    appinputs = dict({
            'input_query': input_text
        })
    result= DocRagCrew().crew().kickoff(inputs=appinputs)

    print("\n\n########################")
    print("## Here is the result")
    print("########################\n")
    print(result)

if __name__ == "__main__":
    run_main()