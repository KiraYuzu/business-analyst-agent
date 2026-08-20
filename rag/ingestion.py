import spacy

from rag.vector_store import add_chunks, delete_document, view_database
from sklearn.metrics.pairwise import cosine_similarity
from rag.embedding import get_embeddings
from pypdf import PdfReader
from pathlib import Path

DOCUMENT_FOLDER = Path("data/company_documents")
nlp = spacy.load("en_core_web_sm")

# Functions for loading of documents
def load_pdf(path):
    reader = PdfReader(path)
    text = ""

    for page in reader.pages:
        text += page.extract_text()

    return text

def load_documents(folder_path):
    documents = []
    folder = Path(folder_path)
    
    for pdf_path in folder.glob("*.pdf"):
        print(f"Loading: {pdf_path.name}")

        text = load_pdf(pdf_path)

        documents.append({
            "filename": pdf_path.name,
            "text": text
        })

    return documents

# Functions for sementic chunking
def sementic_chunking(text):
    # This function is to chunk the text based on semantic meaning rather than just word count.
    sentences = split_into_sentences(text)

    sentence_embeddings = get_sentence_embeddings(sentences)
    similarities = calculate_similarity(sentence_embeddings)

    chunks = create_sementic_chunks(sentences, similarities)

    return chunks

def split_into_sentences(text):
    # Split the text into sentences using spaCy's sentence segmentation
    doc = nlp(text)

    # Filter out empty sentences and strip whitespace
    sentences = [
        sentence.text.strip()
        for sentence in doc.sents
        if sentence.text.strip()  # Only add non-empty sentences
    ]

    return sentences

def get_sentence_embeddings(sentences):
    embeddings = []
    for sentence in sentences:
        embedding = get_embeddings(sentence)
        embeddings.append(embedding)

    return embeddings

def calculate_similarity(embeddings):
    similarities = []

    for i in range(len(embeddings) - 1):
        similarity = cosine_similarity(
            [embeddings[i]],
            [embeddings[i + 1]]
        )[0][0]

        similarities.append(similarity)

    return similarities

def create_sementic_chunks(sentences, similarities, threshold=0.4, max_chunk_words=300, overlap_sentences=1):
    chunks = []
    current_chunk = []
    current_word_count = 0

    for i, sentence in enumerate(sentences):
        sentence_word_count = len(sentence.split())

        # Add the sentence to the current chunk
        current_chunk.append(sentence)
        current_word_count += sentence_word_count

        # Determine whether to create a boundary
        is_last_sentence = i == len(sentences) - 1

        if not is_last_sentence:
            similarity = similarities[i]

            # Sementic boundary
            semantic_boundary = similarity < threshold

            # Max size reached
            max_size_reached = current_word_count >= max_chunk_words

            if semantic_boundary or max_size_reached:
                chunks.append(" ".join(current_chunk))

                # Keep the last few sentences for overlap
                current_chunk = current_chunk[-overlap_sentences:]

                current_word_count = sum(len(sentence.split()) for sentence in current_chunk)

    # Add any remaining sentences as a final chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def ingest_documents():
    print("Starting document ingestion...")

    documents = load_documents(DOCUMENT_FOLDER)

    for document in documents:
        document_name = document["filename"]
        delete_document(document_name)
        chunks = sementic_chunking(document["text"])
        add_chunks(chunks, document_name)

    # View and save database contents
    view_database()

    print("\nIngestion completed!")

if __name__ == "__main__":
    ingest_documents()