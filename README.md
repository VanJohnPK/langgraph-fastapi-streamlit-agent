# 🐹 darkVinci's Agent

Reference: [agent-service-toolkit](https://github.com/JoshuaC215/agent-service-toolkit.git)

## Setup
1. Clone the Repository
2. Install Dependencies
`pip install -r requirements.txt`
3. Set up Environment Variables
    - Create a `.env` file in the root directory.
    - Add your API keys as follows:
    `OPENAI_API_KEY = "your_openai_api_key"`  

## Getting Started
1. You can also run the agent service and the Streamlit app locally without Docker, just using a Python virtual environment.
2. Run the FastAPI server:
`python run_service.py`
3. In a separate terminal, run the Streamlit app:
`streamlit run streamlit_app.py`