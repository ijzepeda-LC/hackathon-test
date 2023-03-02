import openai
import streamlit as st


def summarize(prompt,_model="text-ada-001",language="", verbose=True):
    print(f">>>>>> model {_model}, language: {language}")
    
    augmented_prompt = f"summarize this text {language}: {prompt}"
    try:
        #Saving it to the state, at the same time
        st.session_state['summary'] = openai.Completion.create(
            # model="text-davinci-003", #best 4000 tokens
            model=str(_model), #Cheapest 2049 tokens
            prompt=augmented_prompt,
            temperature=.5,
            max_tokens= 1000 if int(prompt/4)>250 else int(prompt/4),
        )['choices'][0]['text']
    except Exception as e:
        error="There was an error", str(e) if verbose else ""
        print(error)
        # output_text= st.text_area(label="Sumarized text:", value=error, height=250)
        st.session_state['summary'] = error
    