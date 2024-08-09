def split_content_by_paragraph(content, max_chunk_size):
    paragraphs = content.split('\n')
    chunks = []
    current_chunk = []
    current_size = 0

    for paragraph in paragraphs:
        paragraph_size = len(paragraph)
        if current_size + paragraph_size > max_chunk_size and current_chunk:
            chunks.append('\n'.join(current_chunk))
            current_chunk = []
            current_size = 0
        
        current_chunk.append(paragraph)
        current_size += paragraph_size

    if current_chunk:
        chunks.append('\n'.join(current_chunk))

    return chunks