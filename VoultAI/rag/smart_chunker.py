import re


def clean_text(text):
    """
    Clean PDF extracted text while preserving
    useful line boundaries.
    """

    # Remove control characters
    text = re.sub(
        r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]",
        "",
        text
    )

    # Fix words broken by hyphen + newline
    text = re.sub(
        r"(\w)-\s*\n\s*(\w)",
        r"\1\2",
        text
    )

    # Normalize spaces inside lines
    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    # Normalize newlines
    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text.strip()


def split_sections(text):
    """
    Detect numbered sections even when PDF extraction
    has flattened line breaks.

    Example:

    1. About TechVision
    ...
    2. Product Lineup
    ...
    """

    pattern = r"(?=\b\d+\.\s+[A-Z][A-Za-z &\-]+)"

    sections = re.split(
        pattern,
        text
    )

    return [
        section.strip()
        for section in sections
        if section.strip()
    ]


def split_sentences(text):

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def split_large_text(text, chunk_size):

    words = text.split()

    chunks = []
    current = ""

    for word in words:

        if len(current) + len(word) + 1 <= chunk_size:

            current += (
                " " if current else ""
            ) + word

        else:

            if current:
                chunks.append(current)

            current = word

    if current:
        chunks.append(current)

    return chunks


def chunk_section(section, chunk_size):

    # Section fits
    if len(section) <= chunk_size:
        return [section]

    sentences = split_sentences(section)

    chunks = []
    current = ""

    for sentence in sentences:

        # Sentence is too large
        if len(sentence) > chunk_size:

            if current:
                chunks.append(current)
                current = ""

            large_chunks = split_large_text(
                sentence,
                chunk_size
            )

            chunks.extend(
                large_chunks
            )

            continue

        # Sentence fits
        if len(current) + len(sentence) + 1 <= chunk_size:

            current += (
                " " if current else ""
            ) + sentence

        else:

            if current:
                chunks.append(current)

            current = sentence

    if current:
        chunks.append(current)

    return chunks


def add_overlap_to_section_chunks(
    chunks,
    overlap
):

    if overlap <= 0:
        return chunks

    final_chunks = []

    for index, chunk in enumerate(chunks):

        if index == 0:

            final_chunks.append(chunk)
            continue

        previous = chunks[index - 1]

        words = previous.split()

        overlap_words = []
        length = 0

        for word in reversed(words):

            if length + len(word) + 1 > overlap:
                break

            overlap_words.insert(
                0,
                word
            )

            length += len(word) + 1

        overlap_text = " ".join(
            overlap_words
        )

        if overlap_text:

            chunk = (
                overlap_text
                + " "
                + chunk
            )

        final_chunks.append(chunk)

    return final_chunks


def smart_chunk(
    text,
    chunk_size=500,
    overlap=50,
    source="unknown"
):

    text = clean_text(text)

    sections = split_sections(text)

    all_chunks = []

    for section in sections:

        section_chunks = chunk_section(
            section,
            chunk_size
        )

        section_chunks = (
            add_overlap_to_section_chunks(
                section_chunks,
                overlap
            )
        )

        all_chunks.extend(
            section_chunks
        )

    # Create metadata
    documents = []

    for index, chunk in enumerate(all_chunks):

        first_line = chunk.split("\n")[0]

        documents.append({
            "chunk_id": index,
            "text": chunk,
            "section": first_line,
            "source": source
        })

    return documents
    