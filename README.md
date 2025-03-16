# CLAII - Command Line Artifical Intelligence Interface
Shell commands can be annoying to memorise and use, CLAII is here to help you generate your commands without a hassle! Free, Self-hosted, and supports multiple APIs so you can use the model you want!

## Implemented APIs
[y] Ollama
[y] OpenAI
[ ] DeepSeek (Soon)
[ ] Perplexity (Soon)
[ ] Mistral (Soon)
[ ] Gemini (Soon)

## How to install
Coming soon

## How to use
After installation, you need to set a few parameters:

```bash
$ claii set tool (ollama|openai|deepseek|perplexity|mistral|gemini)
```

Then you need to add your key, skip this step if you're using ollama:

```bash
$ claii set key (openai|deepseek|perplexity|mistral|gemini) <key-xxxxx...>
```

If you're using ollama, then set your model:

```bash
$ claii set model "modelname"
```

and now you can start to generate your commands!
```bash
$ claii chat "Make a new directory structure for a react project"

Using Ollama (qwen2.5-coder:1.5b)
AI: pip install -r requirements.txt && python app
```
you can also directly run your commands!
```bash
$ claii chat "Make a new directory structure for a react project" --run

Using Ollama (qwen2.5-coder:1.5b)
AI: pip install -r requirements.txt && python app
Executing command...
```
