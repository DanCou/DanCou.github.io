import argparse
from pathlib import Path


question = ""
answer = ""

question_template = f"""
<details class="question">
<summary>{question}</summary>
{answer}.
</details>
"""

def parse_args():
    parser = argparse.ArgumentParser(description="Parse txt file and generate Markdown output.")

    # Define arguments
    parser.add_argument(
        "filename",
        type=str,
        default=None,
        help="Name of the txt file to be processed."
    )
    return parser.parse_args()



def parse_text(text):
    categories = {"?": [], "!": [], "*": [], "#": []}
    pairs = []  # List to store the (question, answer) pairs

    lines = text.split("\n")
    i = 0
    output = ""
    while i < len(lines):
        s = ""
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        match line[0]:
            case "?":  # If the line starts with "?"
                question = line[1:].strip()  # Get the question text
                # Look for the next line starting with "!"
                if i + 1 < len(lines) and lines[i + 1].strip().startswith("!"):
                    answer = lines[i + 1].strip()[1:].strip()  # Get the answer text
                    pairs.append((question, answer))  # Add the pair (question, answer)
                    
                    s = f'<details class="question">\n<summary>{question}</summary>\n{answer}\n</details>\n'
                        
                    i += 1  # Skip the next line as it's already used


            case "*":  # Store other lines in their respective categories
                data = line[1:].strip()
                if data:
                    s = f'<div class="interest">\n{data}\n</div>\n'
                    categories[line[0]].append(s)


            case "#":  # Store other lines in their respective categories
                data = line[1:].strip()
                if data:
                    s = f'<div class="go">\n{data}\n</div>\n'
                    categories[line[0]].append(s)

            case _:  # Skip lines that don't start with valid symbols
                    s = ""
        output += s

        i += 1  # Move to the next line

    return output, categories, pairs

def main():

    args = parse_args()
    print("running with the following parameters:")
    print(f"   filename = {args.filename}")

    inputfile = Path(args.filename)
    outputfile = Path(args.filename).with_suffix(".md")
    print(outputfile)
    with open(inputfile, "r", encoding="utf8") as file:
        text = file.read()
        output, categories, pairs = parse_text(text)
        # print(categories)
        # print("---")
        # print(pairs)
    with open(outputfile, "w", encoding="utf8") as file:
        file.write(output)

if __name__ == "__main__":
    main()