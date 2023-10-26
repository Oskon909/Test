import argparse
from html.parser import HTMLParser


class MessageSplitter(HTMLParser):
    def __init__(self, max_len):
        super().__init__()
        self.max_len = max_len
        self.fragment = ""
        self.stack = []

    def handle_starttag(self, tag, attrs):
        self.fragment += f"<{tag}>"
        self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag == self.stack[-1]:
            self.fragment += f"</{tag}>"
            self.stack.pop()

    def handle_data(self, data):
        remaining_space = self.max_len - len(self.fragment)
        if remaining_space >= len(data):
            self.fragment += data
        else:
            self.fragment += data[:remaining_space]
            yield self.fragment
            self.fragment = ""

    def split_message(self, source):
        self.feed(source)
        if self.fragment:
            yield self.fragment


def main():
    parser = argparse.ArgumentParser(description="Split an HTML message into fragments.")
    parser.add_argument("--max-len", type=int, help="Maximum length for each fragment")
    parser.add_argument("html_file", help="Path to the HTML file to process")

    args = parser.parse_args()

    max_len = args.max_len

    with open(args.html_file, "r") as file:
        source_html = file.read()

    splitter = MessageSplitter(max_len)
    for fragment in splitter.split_message(source_html):
        print(fragment)


if __name__ == "__main__":
    main()
