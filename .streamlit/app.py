import streamlit as st
import os
import openai
# from functions import summarize
import toml

verbose=True


def summarize(prompt,_model="text-ada-001",language="", verbose=True):
    tokens=int(1000) if int(len(prompt)/4)>250 else int(len(prompt)/4)
    # augmented_prompt = f"summarize this text {language}: {prompt}"
    augmented_prompt = f"summarize this text {language}: {prompt}"
    print(augmented_prompt)
    # st.session_state['summary'] =augmented_prompt
    try:
        #Saving it to the state, at the same time
        st.session_state['summary'] = openai.Completion.create( 
            model =  _model,  
            prompt = augmented_prompt,
            temperature=.5,
            max_tokens= tokens,
        )['choices'][0]['text'].strip()
    except Exception as e:
        error="There was an error", str(e) if verbose else ""
        print(error)
        # output_text= st.text_area(label="Sumarized text:", value=error, height=250)
        st.session_state['summary'] = error
    

def count_words():
    # count words  
    st.session_state['txt_len']= len(st.session_state['mytext'].split())


try:
    openai.api_key = toml.load('secrets.toml')['OPENAI_API_KEY']#os.getenv("OPENAI_API_KEY")
    placeholder_txt="There is this idea in education that everyone has their own preferred way of learning. They're so-called learning style. If information is presented in accordance with the learning style, then they'll learn better. Now there are dozens of different learning style theories, but the most common one identifies four main learning styles. Visual, auditory, reading, writing, and kinesthetic, or VARC for short. Visual learners learn best from images, demonstrations, and pictures. People may say things, but I can't really like take it in. I just got to see them act it out or write it or something. Auditory learners learn best from listening.to an explanation. Reading writing learners learn best from reading and writing. And kinesthetic learners learn best by doing, physically interacting with the world. Hands on, you have to touch things, you have to play with things. It's a contact sport. You have to do it yourself. Now, learning styles make intuitive sense because we know everyone is different. Some people have better spatial reasoning. Others have better listening comprehension. We know some people are better readers while others are good with their hands. It sort of very much fits with a broad strain of thought in the recent Western tradition is. like we're all unique, we're all different. And so you don't want to say like everybody learns the same way. That sort of conflicts with our feelings about what it means to be human. So doesn't it make sense that people should learn better in their own preferred learning style? Well, teachers certainly seem to think so. A survey of nearly 400 teachers from the UK and the Netherlands found that over 90 percent believed that individuals learn better when they receive information in their preferred learning style."


    # Setting session states
    if "summary" not in st.session_state:
        st.session_state['summary'] = ""
    if "model" not in st.session_state:
        st.session_state['model'] = "text-ada-001"
    if "mytext" not in st.session_state:
        st.session_state['mytext'] = placeholder_txt
    if "txt_len" not in st.session_state:
        st.session_state['txt_len']=len(st.session_state['mytext'].split())
    



    st.title("Lecture Summarizer")

    # Select model
    models_text=("Ada (1000 words)","Babbage (2kw)","Curie (2kw)","Davinci (3kw + languages)")
    models=['text-ada-001','text-babbage-001','text-curie-001','text-davinci-003']
    
    model_radio= st.radio("Select GPT model",models_text, horizontal=True)
    #get index from string
    model_=models[models_text.index(model_radio)]
    

    # Select Language output
    if model_radio == "Davinci (3kw + languages)":
        lans_text=('English','Spanish','Hindi','Nepali')
        languages=['','in Spanish','in Hindi','in Nepali']
        language_radio = st.radio("Translate summary:",lans_text, horizontal=True)
        #get index from string
        language_=languages[lans_text.index(language_radio)]
    else:
        language_=""

    input_text = st.text_area(label='Enter full text:', value=placeholder_txt, height=250, key="mytext",on_change=count_words)

    st.text(str(st.session_state['txt_len'])+" words")

    st.button("Submit",
            on_click=summarize,
            kwargs={"prompt":input_text,'_model':model_, 'language':language_, 'verbose':verbose}, # the argument  ssent to onclick function
            )

    # fill text area with current state of summary
    output_text= st.text_area(label="Sumarized text:", value=st.session_state['summary'], height=250)


except Exception as e:
    print("There was an error", str(e) if verbose else "")
    



# """
# This model's maximum context length is 2049 tokens, 
# however you requested 3360 tokens 
# (2960 in your prompt; 400 for the completion).
#  Please reduce your prompt; or completion length.
# """