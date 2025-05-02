import gradio as gr
from SkyFlareCore import SkyFlareCore
import os

skyflare:SkyFlareCore = None

def init():
     with gr.Blocks() as demo:
        ci = gr.ChatInterface(fn=respond,
                           clear_btn="Clear",
                           title="skyflare: " + skyflare.user_name,
                           autofocus=True)
        ta = gr.TextArea('none')
        out = gr.TextArea()
        ci.chatbot.change(report_skyflare, ta, out)
     return demo

def respond(message, chat_history):
            global skyflare
            response = skyflare.chatbot(message, chat_history)
            s = skyflare.to_string_self()
            return response
def report_skyflare(*args):
     global skyflare
     if(skyflare is not None):
          return skyflare.to_string_self()
     return 'Nothing to output'

if __name__ == "__main__":
    current_directory = os.path.dirname(os.path.abspath(__file__))
    print("\n*Welcome to Your ChatApp*\n")
    user = input("Account Username: ")
    check = True
    programCheck = True
    user_path = "userfiles"
    file_name = "{}.txt".format(user)
    file_path = os.path.join(current_directory, user_path, file_name)

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            first_lineCheck = file.readline(5_000_000)
            while check:
                passWord = input("Account Password: ")
                if first_lineCheck.strip() == passWord.strip():
                    print(">>>Welcome to your Data<<<")
                    check = False
                else:
                    print("Wrong Password")
    else:
        with open(file_path, "w") as file:
            print("Account Doesn't exist\nCreating...")
            passWord = input("Create account Password: ")
            file.write("{}\n".format(passWord))
    skyflare = SkyFlareCore(user_name=user)
    # r = skyflare.chatbot("hello", [])
    # print(r)

    init().launch()
    print("Demo launched on http://localhost:7860")

