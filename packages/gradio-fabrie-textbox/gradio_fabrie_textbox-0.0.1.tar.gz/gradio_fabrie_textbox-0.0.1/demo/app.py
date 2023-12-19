
import gradio as gr
from gradio_fabrie_textbox import Fabrie_Textbox


example = Fabrie_Textbox().example_inputs()

demo = gr.Interface(
    lambda x:x,
    Fabrie_Textbox(),  # interactive version of your component
    Fabrie_Textbox(),  # static version of your component
    # examples=[[example]],  # uncomment this line to view the "example version" of your component
)


demo.launch()
