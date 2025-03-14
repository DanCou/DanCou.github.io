
question = ""
answer = ""

question_template = f"""
<details class="question">
<summary>{question}</summary>
{answer}.
</details>
"""


def parse_text(text):
    categories = {"?": [], "!": [], "*": [], "#": []}
    pairs = []  # List to store the (question, answer) pairs

    lines = text.split("\n")
    i = 0
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
                    
                    s = f"""
                        <details class="question">
                        <summary>{question}</summary>
                        {answer}.
                        </details>
                        """
                    i += 1  # Skip the next line as it's already used


            case "*":  # Store other lines in their respective categories
                data = line[1:].strip()
                if data:
                    s = f"""
                        <div class="interest">
                        {data}
                        </div>
                        """
                    categories[line[0]].append(s)


            case "#":  # Store other lines in their respective categories
                data = line[1:].strip()
                if data:
                    s = f"""
                        <div class="go">
                        {data}
                        </div>
                        """
                    categories[line[0]].append(s)

            case _:  # Skip lines that don't start with valid symbols
                    s = ""
        print(s)

        i += 1  # Move to the next line

    return categories, pairs

def main():
    with open("29-convention-montparnasse.txt", "r") as file:
        text = file.read()
        categories, pairs = parse_text(text)
        # print(categories)
        # print("---")
        # print(pairs)


if __name__ == "__main__":
    main()