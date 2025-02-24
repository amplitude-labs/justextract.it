import re


def chunk(text: str, max_words_per_chunk: int = 50) -> list[str]:
    """
    Splits the input text into chunks based on sentences using a simple regex 
    for sentence segmentation. Each chunk contains at most 'max_words_per_chunk' words.

    :param text: The full text to be chunked.
    :param max_words_per_chunk: Maximum number of words allowed per chunk.
    :return: A list of text chunks.
    """
    # Naively split the text into sentences using punctuation as delimiters.
    # This regex splits at punctuation marks (., !, or ?) that are followed by whitespace.
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())

    chunks = []
    current_chunk = []
    current_count = 0

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        words_in_sentence = sentence.split()
        sentence_length = len(words_in_sentence)

        # If the sentence alone exceeds the word limit, break it into sub-chunks.
        if sentence_length > max_words_per_chunk:
            # Finalize any existing chunk first.
            if current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_count = 0

            # Break the long sentence into sub-chunks.
            for i in range(0, sentence_length, max_words_per_chunk):
                sub_chunk_words = words_in_sentence[i:i + max_words_per_chunk]
                chunks.append(" ".join(sub_chunk_words))
        else:
            # If adding the sentence won't exceed the word limit, append it.
            if current_count + sentence_length <= max_words_per_chunk:
                current_chunk.extend(words_in_sentence)
                current_count += sentence_length
            else:
                # Otherwise, finalize the current chunk and start a new one.
                if current_chunk:
                    chunks.append(" ".join(current_chunk))
                current_chunk = words_in_sentence[:]
                current_count = sentence_length

    # Flush any remaining words.
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks
