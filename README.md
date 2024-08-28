# 🦜 🐹's Agent

Reference: [agent-service-toolkit](https://github.com/JoshuaC215/agent-service-toolkit.git)

## Setup
1. Clone the Repository
2. Install Dependencies
`pip install -r requirements.txt`
3. Set up Environment Variables
    - Create a `.env` file in the root directory.
    - Add your API keys as follows:
    ```
    OPENAI_API_KEY = "your_openai_api_key"

    # Optional, to enable Azure service
    AZURE_OPENAI_ENDPOINT = "https://xxx.openai.azure.com/"
    OPENAI_API_VERSION = "2024-02-01"
    AZURE_OPENAI_API_KEY = "xxx"

    # Optional, to enable LangSmith tracing
    LANGCHAIN_TRACING_V2=true
    LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
    LANGCHAIN_API_KEY=your_langchain_api_key
    LANGCHAIN_PROJECT=your_project
    ```  

## Getting Started
1. You can also run the agent service and the Streamlit app locally without Docker, just using a Python virtual environment.
2. Run the FastAPI server:
`python run_service.py`
3. In a separate terminal, run the Streamlit app:
`streamlit run streamlit_app.py`