import gradio as gr
import requests
import json
from gradio.themes.utils import colors, fonts, sizes

OLLAMA_API_URL = "http://localhost:11434/api"

def get_models():
    """
    Retrieve the list of available models from the Ollama API.

    Returns:
        list: A list of model names.
    """
    try:
        response = requests.get(f"{OLLAMA_API_URL}/tags")
        response.raise_for_status()
        models = response.json().get("models", [])
        return [model["name"] for model in models]
    except requests.RequestException as e:
        print(f"Error retrieving models: {e}")
        return []

def poetry_generation_interface(prompt, style, theme, length, model_name):
    """
    Generate a poem using the specified model and style.
    Handles streaming responses from Ollama properly.

    Args:
        prompt (str): The user's prompt for the poem.
        style (str): The style of the poem (e.g., Haiku, Free Verse).
        theme (str): The theme of the poem.
        length (int): The length of the poem.
        model_name (str): The name of the model to use for generating the poem.

    Returns:
        str: The generated poem or an error message if the generation fails.
    """
    try:
        full_prompt = f"{prompt} in the style of a {style}, with a theme of {theme}, and a length of {length} lines."
        response = requests.post(f"{OLLAMA_API_URL}/generate", json={
            "model": model_name,
            "prompt": full_prompt
        }, stream=True)

        response.raise_for_status()

        poem_text = ""  # Accumulate responses here
        for line in response.iter_lines():
            if line:
                try:
                    json_line = json.loads(line)
                    poem_text += json_line.get("response", "")
                except json.JSONDecodeError:
                    print(f"Warning: Could not parse line as JSON: {line}")

        return poem_text.strip() if poem_text else "Error: No response from API"
    
    except requests.RequestException as e:
        print(f"Error in poetry generation interface: {e}")
        return "Error: Unable to generate poetry"

# Define Gradio interface
model_names = get_models()

css = """
@keyframes matrix-glow {
    0% { box-shadow: 0 0 5px #00ff00, 0 0 10px #00ff00, 0 0 15px #00ff00; }
    50% { box-shadow: 0 0 10px #00ff00, 0 0 20px #00ff00, 0 0 30px #00ff00; }
    100% { box-shadow: 0 0 5px #00ff00, 0 0 10px #00ff00, 0 0 15px #00ff00; }
}

@keyframes matrix-fade {
    0% { opacity: 0.8; }
    50% { opacity: 1; }
    100% { opacity: 0.8; }
}

.gradio-container {
    background-color: #000000 !important;
    background-image: linear-gradient(rgba(0, 255, 0, 0.03) 1px, transparent 1px),
                      linear-gradient(90deg, rgba(0, 255, 0, 0.03) 1px, transparent 1px) !important;
    background-size: 20px 20px !important;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    width: 100%;
    padding: 0;
    margin: 0;
}

#chat-container {
    display: flex;
    flex-direction: column;
    height: 750px;
    width: 1000px;
    max-width: 100%;
    margin: 0 auto;
    padding: 10px;
    background: rgba(0, 0, 0, 0.9);
    color: #00ff00;
    border-radius: 10px;
    border: 1px solid #00ff00;
    box-shadow: 0 0 20px #00ff00;
    position: relative;
    animation: matrix-glow 2s infinite;
}

#chat-interface {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow-y: auto;
    padding: 10px;
    background: rgba(0, 10, 0, 0.95);
    border: 1px solid #00ff00;
    border-radius: 5px;
    box-shadow: inset 0 0 10px #00ff00;
    color: #00ff00;
    width: 100%;
}

#model-dropdown {
    border: 1px solid #00ff00;
    border-radius: 5px;
    padding: 5px;
    background: rgba(0, 20, 0, 0.9);
    color: #00ff00;
    font-family: 'Courier New', monospace;
    margin-bottom: 15px;
    width: 100%;
}

.message {
    background: rgba(0, 20, 0, 0.7) !important;
    border: 1px solid #00ff00 !important;
    border-radius: 5px !important;
    padding: 10px !important;
    margin: 5px 0 !important;
    box-shadow: 0 0 5px #00ff00 !important;
}

.user-message {
    background: rgba(0, 40, 0, 0.7) !important;
}

.assistant-message {
    background: rgba(0, 20, 0, 0.7) !important;
}

button {
    background: rgba(0, 40, 0, 0.9) !important;
    border: 1px solid #00ff00 !important;
    color: #00ff00 !important;
    box-shadow: 0 0 10px #00ff00 !important;
    transition: all 0.3s ease !important;
}

button:hover {
    background: rgba(0, 60, 0, 0.9) !important;
    box-shadow: 0 0 20px #00ff00 !important;
}

textarea, input[type="text"] {
    background: rgba(0, 20, 0, 0.9) !important;
    border: 1px solid #00ff00 !important;
    color: #00ff00 !important;
    font-family: 'Courier New', monospace !important;
    box-shadow: inset 0 0 5px #00ff00 !important;
}

textarea:focus, input[type="text"]:focus {
    box-shadow: inset 0 0 10px #00ff00, 0 0 10px #00ff00 !important;
    outline: none !important;
}

.feedback {
    color: #00ff00 !important;
    text-shadow: 0 0 5px #00ff00 !important;
}

footer {
    display: none !important;
}

::-webkit-scrollbar {
    width: 10px;
    background: rgba(0, 20, 0, 0.9);
}

::-webkit-scrollbar-thumb {
    background: #00ff00;
    border-radius: 5px;
    box-shadow: 0 0 5px #00ff00;
}
"""

class CustomDarkTheme(gr.themes.Base):
    """
    Custom dark theme for the Gradio interface.
    """
    def __init__(self):
        super().__init__(
            primary_hue=colors.green,
            secondary_hue=colors.green,
            neutral_hue=colors.gray,
            spacing_size=sizes.spacing_md,
            radius_size=sizes.radius_md,
            text_size=sizes.text_md,
            font=["Courier New", "monospace"],
            font_mono=["Courier New", "monospace"]
        )
        self.set(
            body_background_fill="#000000",
            body_background_fill_dark="#000000",
            body_text_color="#00ff00",
            body_text_color_dark="#00ff00",
            body_text_size="*text_md",
            color_accent="#00ff00",
            color_accent_soft="#003300",
            border_color_primary="#00ff00",
            background_fill_primary="#000000",
            block_background_fill="#000000",
            block_label_background_fill="*color_accent_soft",
            block_label_text_color="#00ff00",
            input_background_fill="#001100",
            input_border_color="#00ff00",
            button_primary_background_fill="#003300",
            button_primary_text_color="#00ff00",
            button_primary_border_color="#00ff00",
            button_secondary_background_fill="#001100",
            button_secondary_text_color="#00ff00",
            button_secondary_border_color="#00ff00",
            block_title_text_color="#00ff00",
            prose_text_size="*text_md",
            prose_text_weight="400",
            prose_header_text_weight="600"
        )

with gr.Blocks(css=css, theme=CustomDarkTheme()) as demo:
    demo.queue()
    with gr.Column(elem_id="chat-container"):
        with gr.Column(elem_id="chat-interface"):
            model_dropdown = gr.Dropdown(model_names, label="Select Model", elem_id="model-dropdown")
            poem_style = gr.Dropdown(["Haiku", "Free Verse", "Sonnet", "Limerick"], label="Select Poem Style", elem_id="poem-style-dropdown")
            poem_theme = gr.Textbox(label="Poem Theme", elem_id="poem-theme")
            poem_length = gr.Slider(1, 100, label="Poem Length (lines)", elem_id="poem-length")
            poetry_interface_component = gr.Interface(
                fn=poetry_generation_interface,
                inputs=["text", poem_style, poem_theme, poem_length, model_dropdown],
                outputs="text",
                title="Poetry Generation Interface"
            )

    def poetry_interface_wrapper(prompt, style, theme, length, model_name):
        """
        Wrapper function for the poetry generation interface.

        Args:
            prompt (str): The user's prompt for the poem.
            style (str): The style of the poem (e.g., Haiku, Free Verse).
            theme (str): The theme of the poem.
            length (int): The length of the poem.
            model_name (str): The name of the model to use for generating the poem.

        Returns:
            str: The generated poem or an error message if the generation fails.
        """
        return poetry_generation_interface(prompt, style, theme, length, model_name)

    poetry_interface_component.fn = poetry_interface_wrapper

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7866,
        root_path="/gradio-poetry"  # This makes it work behind the Nginx proxy
    )
