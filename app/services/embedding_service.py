from langchain_core.embeddings import Embeddings
from langchain_huggingface import HuggingFaceEmbeddings

from app.core.config import settings

def get_embeddings_model() -> Embeddings:                                                                                                           
    return HuggingFaceEmbeddings(                                                                                                                   
        model_name=settings.HUGGINGFACE_EMBEDDING_MODEL,                                                                                            
        model_kwargs={"device": settings.HUGGINGFACE_EMBEDDING_DEVICE},                                                                             
        encode_kwargs={                                                                                                                             
            "normalize_embeddings": settings.HUGGINGFACE_NORMALIZE_EMBEDDINGS,                                                                      
        },                                                                                                                                          
    ) 