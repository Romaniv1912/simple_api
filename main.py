from pathlib import Path

import uvicorn

from src.core.registrar import register_app

app = register_app()


if __name__ == '__main__':
    uvicorn.run(f'{Path(__file__).stem}:app', host='0.0.0.0', port=8000, reload=True)
