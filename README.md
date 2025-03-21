# **CLAII - Command Line Artificial Intelligence Interface**  

Shell commands can be **frustrating to memorize and use**—**CLAII** is here to help!  
Generate, refine, and **execute** commands **effortlessly** with free, **self-hosted AI**.  

✅ **Fast & Lightweight**  
✅ **Self-Hosted** (Ollama support)  
✅ **Supports Multiple AI APIs**  

---

## **All the APIs you need!**  

CLAII supports **all major AI APIs**, so you can choose the best model for your needs:  

| Model       | Status    | Notes |
|-------------|----------|--------|
| **Ollama**  | ✅ Supported | Local & self-hosted |
| **OpenAI**  | ✅ Supported | Requires API key |
| **DeepSeek** | ✅ Supported | Requires API key |
| **Perplexity** | ✅ Supported | Requires API key |
| **Mistral** | ✅ Supported | Requires API key |
| **Gemini** | ✅ Supported | Requires API key |

---

## **How CLAII Works**  

CLAII allows you to:  

1. **Generate shell commands** from natural language.  
2. **Refine commands** with AI assistance.  
3. **Execute commands directly** (optional).  

### **Example Usage**  

```bash
claii chat "Create a React project with Vite and Tailwind"
```

#### **Example Output**  

```bash
Using Ollama (qwen2.5-coder:1.5b)
AI: npm create vite@latest my-app && cd my-app && npm install tailwindcss postcss autoprefixer && npx tailwindcss init -p
```

### **Run the Command Automatically**  

```bash
claii chat "Create a React project with Vite and Tailwind" --run
```

#### **Example Output**  

```bash
Using Ollama (qwen2.5-coder:1.5b)
AI: npm create vite@latest my-app && cd my-app && npm install tailwindcss postcss autoprefixer && npx tailwindcss init -p
Executing command...
```

---

## **Installation**  

### **📥 Method 1: Download the Wheel File (Recommended)**  
Download the latest **`.whl`** file from [GitHub Releases](https://github.com/YoussefAlkentclaii/releases) and install it using:  

```bash
pip install path/to/claii-x.x.x-py3-none-any.whl
```

### **📦 Method 2: Install from PyPI**  
You can now download and install CLAII directly from pip! 

```bash
pip install claii-ai
```

### **🎩 Method 3: Install from the AUR (Coming Soon)**  
For **Arch Linux** users, an **AUR package** will be available soon.

---

## **Configuration**  

Before using CLAII, set up your preferred AI tool.  

### **1️⃣ Select Your AI Tool**  

```bash
claii config set tool (ollama|openai|deepseek|perplexity|mistral|gemini)
```

### **2️⃣ Set Your API Key (If Required)**  

If you're **not** using Ollama, you **must** provide an API key:  

```bash
claii config set key (openai|deepseek|perplexity|mistral|gemini) <your_api_key>
```

### **3️⃣ Set Your Ollama Model (If Using Ollama)**  

If using Ollama, specify your **local model**:  

```bash
claii config set model "mistral"
```

---

## **Features & Roadmap**  

| Feature                 | Status    | Notes |
|-------------------------|----------|--------|
| **Generate shell commands** | ✅ Done | Works with all supported models |
| **Refine existing commands** | ✅ Done | AI improves or corrects commands |
| **Run commands automatically** | ✅ Done | Use `--run` flag to execute |
| **Support for DeepSeek AI** | ✅ Done | Requires API key |
| **Support for Perplexity AI** | ✅ Done | Requires API key |
| **Support for Mistral AI** | ✅ Done | Requires API key |
| **Support for Gemini AI** | ✅ Done | Requires API key |
| **AUR Package** | 🔜 Coming Soon | Arch Linux package |
| **PyPI Release** | ✅ Done | Install via `pip install claii-ai` |

---

### 🚀 **CLAII makes shell commands effortless!** 🚀  

## **Features**

- **Multi-model support**: Easily switch between different AI models (OpenAI, Ollama, Perplexity, Mistral, Gemini, DeepSeek)
- **Plugin system**: Extend CLAII with custom commands, AI models, and tools
- **Simple configuration**: Easy-to-use config commands for API keys and model selection
- **Command system**: Well-organized command structure for different operations

## **Usage**

### **Basic Chat**

```bash
claii chat "Your message here"
```

### **Using a Specific AI Model**

```bash
claii chat "Your message here" --tool openai
claii chat "Your message here" --tool ollama
claii chat "Your message here" --tool mistral
# And more!
```

### **Configuration**

```bash
# Set API keys
claii config set key openai your_api_key

# Set models
claii config set model ollama llama3

# View configuration
claii config get-all
```

## **Plugin System**

CLAII includes a flexible plugin system for extending its functionality:

### **Managing Plugins**

```bash
# List all available plugins
claii system list-plugins

# Enable a plugin
claii system enable-plugin plugin_name

# Disable a plugin
claii system disable-plugin plugin_name
```

### **Using Plugin Models**

```bash
# Use a model provided by a plugin
claii chat "Your message" --tool plugin_model_name
```

### **Plugin Documentation**

For more information on using and creating plugins, see:

- [Plugin Quickstart Guide](claii/docs/PLUGINS_QUICKSTART.md)
- [Full Plugin Documentation](claii/docs/plugins.md)
- [Example Plugins](claii/docs/examples/plugins/)

### **Contributers**
- @AdhamAfis for his incredible work on the plugin system.

## **License**

MIT
