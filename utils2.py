import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
#from pruebagroq import Groq
import os
from sentence_transformers import SentenceTransformer
from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()

api_key=os.getenv("OPENAI_API_KEY")

def responderquery(query):


    ##################
    

    ##########
    querynuevo = query[-1]['content']
    historialcompleto=query.pop()
    # Accedemos al contenido de la lista 'query'
    
    #os.environ["GROQ_API_KEY"] ="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"
    model=SentenceTransformer('distiluse-base-multilingual-cased-v2')
    #cargar dataframe con los embeddings y chunks
    chunks_df=pd.read_pickle("chunks_embeddings.pkl")
    
    
    

    
    def retrieve_relevant_chunks(query_embedding,chunks_df ,top_k=5):
        
              embeddings_matrix=np.vstack(chunks_df["embeddings"].values)
              similarities=cosine_similarity([query_embedding], embeddings_matrix)[0]
              #invertimos el valor de los indices, ya que argsort los hace de menor a mayor, recuperamos asi los 5 mayores
              top_k_indices = similarities.argsort()[-top_k:][::-1]
              chunks_relevant=chunks_df.iloc[top_k_indices]
              return chunks_relevant
    """
    input("esto es el query nuevo inicio")
    print(querynuevo)
    input("esto es el query nuevo")
    print(query)
    input("esto es el historial ")
    """
    def generar_respuesta(query,relevant_chunks):
        context="/n".join(relevant_chunks["chunks"].tolist())
     
        client = OpenAI()             
        #client = Groq()
        chat_completion = client.chat.completions.create(
        
        # Required parameters
        #
         messages=[
        # Set an optional system message. This sets the behavior of the
        # assistant and can be used to provide specific instructions for
        # how it should behave throughout the conversation.
        {
            "role": "system",
            "content": "Eres un bot diseñado para dar respuestas basadas solo en una base de datos sobre rubricas ya evaluadas, tu trabajo es buscar alumnos para recomendarlos basandote en los campos Nombre Rubricas y Descripcion Rubricas, ya que necesitan alumnos (fijate en el campo nombre alumno) para proyectos, siempre menciona los datos de las rubricas y forma la respuesta}"
        },
        
        # Set a user message for the assistant to respond to.
        {
            "role": "user",
            "content": f"{query}\n\nContexto relevante:\n{context}",
        }
    ],
    
        # The language model which will generate the completion.
        model="gpt-3.5-turbo",
    
        #
        # Optional parameters
        #
    
        # Controls randomness: lowering results in less random completions.
        # As the temperature approaches zero, the model will become deterministic
        # and repetitive.
        temperature=0.5,
    
        # The maximum number of tokens to generate. Requests can use up to
        # 32,768 tokens shared between prompt and completion.
        max_tokens=1024,
    
        # Controls diversity via nucleus sampling: 0.5 means half of all
        # likelihood-weighted options are considered.
        top_p=1,
    
        # A stop sequence is a predefined or user-specified text string that
        # signals an AI to stop generating content, ensuring its responses
        # remain focused and concise. Examples include punctuation marks and
        # markers like "[end]".
        stop=None,
    
        # If set, partial message deltas will be sent.
        stream=False,
        )
        #print(query_embedding)
        return chat_completion.choices[0].message.content
    
    
    query_embedding=model.encode(querynuevo)
    relevant_chunks=retrieve_relevant_chunks(query_embedding,chunks_df)

   
    respuestanueva=generar_respuesta(query,relevant_chunks)

    #querynuevo
    #respuestanueva

    return (respuestanueva)
        # Print the completion returned by the LLM.
    

#print(responderquery(query="que paso con Rafael Cespedes"))
