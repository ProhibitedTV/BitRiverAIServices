# Gradio Interfaces for Chat and Poetry Generation

This project contains two separate Gradio interfaces for chat and poetry generation using locally installed Ollama models. Each interface runs on a different port and can be accessed individually.

## Requirements

Ensure you have the required dependencies installed. You can install them using the provided `requirements.txt` file:

```sh
pip install -r requirements.txt
```

## Interfaces

### Chat Interface

The chat interface allows users to interact with different models for chat-based responses.

- **File:** `chat_app.py`
- **Port:** 7861

#### Running the Chat Interface

```sh
python /home/rhythmic/Gradio/chat_app.py
```

### Poetry Generation Interface

The poetry generation interface allows users to generate poetry based on prompts.

- **File:** `poetry_app.py`
- **Port:** 7863

#### Running the Poetry Generation Interface

```sh
python /home/rhythmic/Gradio/poetry_app.py
```

## Accessing the Interfaces

Once the interfaces are running, you can access them in your web browser using the following URLs:

- **Chat Interface:** [http://127.0.0.1:7861](http://127.0.0.1:7861)
- **Poetry Generation Interface:** [http://127.0.0.1:7863](http://127.0.0.1:7863)

## Notes

- Ensure your Ollama server is running locally and accessible at `http://localhost:11434`.
- If you encounter memory issues with the models, consider selecting a smaller model or adjusting the model parameters to reduce memory usage.
