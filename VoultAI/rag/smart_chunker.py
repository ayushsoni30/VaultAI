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
    Detect numbered sections.

    Examples:
        1. About TechVision
        2. Product Lineup
        3. Core Features
        4. Customer Use Cases
    """

    pattern = r"(?=\b\d+\.\s+[A-Z][A-Za-z0-9 &,\-]+)"

    sections = re.split(pattern, text)

    return [
        section.strip()
        for section in sections
        if section.strip()
    ]


def split_sentences(text):
    """
    Split text into sentences.
    """

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
    """
    Split a sentence that is larger than chunk_size
    without breaking words.
    """

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
    """
    Split a section into smaller chunks while
    preserving the section heading.
    """

    lines = section.split("\n")

    # First line is treated as section heading
    heading = lines[0].strip()

    body = "\n".join(lines[1:]).strip()

    # If entire section fits
    if len(section) <= chunk_size:
        return [section]

    sentences = split_sentences(body)

    chunks = []
    current = ""

    for sentence in sentences:

        # Sentence itself is too large
        if len(sentence) > chunk_size:

            if current:

                chunks.append(
                    heading + "\n" + current
                )

                current = ""

            large_chunks = split_large_text(
                sentence,
                chunk_size - len(heading) - 1
            )

            for large_chunk in large_chunks:

                chunks.append(
                    heading + "\n" + large_chunk
                )

            continue

        # Sentence fits current chunk
        if (
            len(current)
            + len(sentence)
            + 1
            + len(heading)
            + 1
            <= chunk_size
        ):

            current += (
                " " if current else ""
            ) + sentence

        else:

            if current:

                chunks.append(
                    heading + "\n" + current
                )

            current = sentence

    # Last chunk
    if current:

        chunks.append(
            heading + "\n" + current
        )

    return chunks


def add_overlap_to_section_chunks(
    chunks,
    overlap
):
    """
    Add overlap between chunks.

    The overlap is taken from the previous chunk.
    """

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

            # Don't duplicate heading
            lines = chunk.split("\n", 1)

            if len(lines) == 2:

                heading = lines[0]
                body = lines[1]

                chunk = (
                    heading
                    + "\n"
                    + overlap_text
                    + " "
                    + body
                )

            else:

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
    """
    Main smart chunking pipeline.
    """

    # Step 1: Clean text
    text = clean_text(text)

    # Step 2: Detect sections
    sections = split_sections(text)

    all_chunks = []

    # Step 3: Process every section
    for section in sections:

        section_chunks = chunk_section(
            section,
            chunk_size
        )

        # Step 4: Add overlap
        section_chunks = (
            add_overlap_to_section_chunks(
                section_chunks,
                overlap
            )
        )

        all_chunks.extend(
            section_chunks
        )

    # Step 5: Create metadata
    documents = []

    for index, chunk in enumerate(all_chunks):

        lines = chunk.split("\n")

        section = lines[0].strip()

        documents.append({
            "chunk_id": index,
            "text": chunk,
            "section": section,
            "source": source
        })

    return documents