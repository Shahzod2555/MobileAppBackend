from src import create_app
import uvicorn

run_app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:run_app", reload=True, log_level = "warning")
