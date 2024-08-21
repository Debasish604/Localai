import gradio as gr
import requests
import json

def get_response_from_api(message):
    url = "http://localhost:11434/api/chat"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "llama3.1:8b",
        "messages": [
            {
                "role": "user",
                "content": message
            }
        ]
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        raw_response = response.text
        print("Raw Response Text:", raw_response)  # Debugging line
        
        # Split the response text by new lines and parse each line as a JSON object
        bot_message_parts = []
        for line in raw_response.strip().split('\n'):
            if line.strip():  # Avoid empty lines
                response_json = json.loads(line)
                message_content = response_json.get('message', {}).get('content', '')
                bot_message_parts.append(message_content)

        bot_message = ''.join(bot_message_parts)
        
    except ValueError as e:
        print(f"JSON decode error: {e}")  # This will catch JSON formatting issues
        bot_message = "Sorry, the response was not in a valid JSON format."
    except Exception as e:
        print(f"An exception occurred: {e}")
        bot_message = "Sorry, I'm unable to reach the server right now."
    
    return bot_message

def chat_with_bot(message, chat_history):
    bot_message = get_response_from_api(message)
    chat_history.append((message, bot_message))
    return "", chat_history

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.ClearButton([msg, chatbot])

    msg.submit(chat_with_bot, [msg, chatbot], [msg, chatbot])

if __name__ == "__main__":
    demo.launch(server_port=3008)
