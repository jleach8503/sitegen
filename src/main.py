from textnode import TextType, TextNode

def main():
    text = TextNode("This is a link",TextType("link"),"https://www.boot.dev")
    print(text)

if __name__ == "__main__":
    main()