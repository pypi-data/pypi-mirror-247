
import gradio as gr
from gradio_mycomponent3 import MyComponent3


example = MyComponent3().example_inputs()

demo = gr.Interface(
    lambda x:x,
    MyComponent3(),  # interactive version of your component
    MyComponent3(),  # static version of your component
    # examples=[[example]],  # uncomment this line to view the "example version" of your component
)


demo.launch()
