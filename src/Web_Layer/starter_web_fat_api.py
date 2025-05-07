from src.Web_Layer.map_fast_api import RestFastAPI

# Create an importable FastAPI app instance
rest_api_instance = RestFastAPI()
app = rest_api_instance.app  # Expose the FastAPI `app` instance globally


class Starter:
    def __init__(self):
        self.api = rest_api_instance  # Use the global RestFastAPI instance

    def run(self):
        import uvicorn

        # Pass the app import string instead of the app object
        uvicorn.run("starter_web_fat_api:app", host="0.0.0.0", port=8001, reload=True)


# If running as the main script
if __name__ == "__main__":
    starter = Starter()
    starter.run()
