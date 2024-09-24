import tiktoken


def get_tokens(words: str) -> int:
    encoding = tiktoken.get_encoding("cl100k_base")
    # encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = encoding.encode(words)
    return len(tokens)
