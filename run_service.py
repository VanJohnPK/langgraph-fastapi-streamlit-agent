import uvicorn
from service import app

uvicorn.run(app, host="0.0.0.0", port=81)
