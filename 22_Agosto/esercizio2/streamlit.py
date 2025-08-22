import streamlit as st

# Check if 'counter' already exists in session_state
# If not, then initialize it
# Ogni volta che premiamo un qualsiasi bottone nella pagina web
# Streamlit riesegue tutta l'intera pagina e quindi si perdono gli "aggiornamenti" fatti agli attributi, 
# Per rendere persistenti i dati tra le varie escuzioni, si utilizza session_state, che invece è condiviso 
# tra le varie sessioni, perciò tutte quante le sessioni leggeranno i valori presenti in quel dizionario
if "counter" not in st.session_state:
    st.session_state.counter = 0        # sessions_state è un dizionario, potrei perciò inserire sia la chiave che il valore così: st.session_state['counter'] = 0

# Funzioni per aumentare o diminuire
def increment():
    st.session_state.counter += 1

def decrement():
    st.session_state.counter -= 1

# Impostiamo titolo
st.title("Counter")

# Pulsanti e numero
st.button("Decrement (-)", on_click=decrement)
st.write(st.session_state.counter)
st.button("Increment (+)", on_click=increment)


# Sidebar
st.sidebar.title("Sidebar")
nome = st.sidebar.text_input("Inserisci il tuo nome: ") # conterrà ciò che l'utente digita

if nome:
    st.sidebar.write(f"Ciao {nome}!")
