from transformers import pipeline
import torch
from functools import lru_cache
import os

# Use smaller T5 model instead of BART for lower memory usage
MODEL_NAME = "sshleifer/distilbart-cnn-6-6"  # Smaller model, ~280MB

# Initialize the summarization pipeline with optimized settings
summarizer = pipeline(
    "summarization",
    model=MODEL_NAME,
    device=-1,  # Force CPU usage since Heroku has no GPU
    model_kwargs={"low_cpu_mem_usage": True}
)

@lru_cache(maxsize=100)  # Cache last 100 summaries to save processing
def _generate_chunk_summary(text: str, max_length: int, min_length: int) -> str:
    """Generate summary for a single chunk with caching"""
    try:
        result = summarizer(text, 
                          max_length=max_length,
                          min_length=min_length,
                          do_sample=False)
        return result[0]['summary_text']
    except Exception as e:
        print(f"Chunk summarization error: {str(e)}")
        return ""

def generate_summary(text, max_length=130, min_length=30):
    """
    Generate a summary using DistilBART model with optimizations for Heroku.
    
    Args:
        text (str): The input text to summarize
        max_length (int): Maximum length of the summary
        min_length (int): Minimum length of the summary
    
    Returns:
        str: The generated summary
    """
    try:
        # Optimize chunk size for memory constraints
        max_chunk_length = 512  # Reduced from 1024 to save memory
        
        # Split text into smaller chunks
        chunks = [text[i:i + max_chunk_length] for i in range(0, len(text), max_chunk_length)]
        
        # Process chunks with size validation
        summaries = []
        for chunk in chunks:
            if len(chunk.strip()) < 50:  # Skip very short chunks
                continue
            
            # Get cached or generate new summary for chunk
            chunk_summary = _generate_chunk_summary(chunk.strip(), max_length, min_length)
            if chunk_summary:
                summaries.append(chunk_summary)
        
        # Combine summaries intelligently
        if not summaries:
            return None
            
        final_summary = " ".join(summaries)
        
        # Ensure reasonable length
        if len(final_summary) > 4000:  # Telegram message limit
            final_summary = final_summary[:3997] + "..."
            
        return final_summary
        
    except Exception as e:
        print(f"Summarization error: {str(e)}")
        return None

# Clear cache periodically to prevent memory buildup
def clear_summary_cache():
    _generate_chunk_summary.cache_clear() 