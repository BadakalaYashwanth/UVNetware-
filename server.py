import os
import subprocess
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import time

app = FastAPI()

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

INPUT_FILE = 'data/raw/real_world_input.json'
OUTPUT_FILE = 'output_insights.json'

class AnalyticsInput(BaseModel):
    data: dict

@app.get("/api/input")
async def get_input():
    if not os.path.exists(INPUT_FILE):
        raise HTTPException(status_code=404, detail="Input file not found")
    with open(INPUT_FILE, "r") as f:
        return json.load(f)

@app.get("/api/output")
async def get_output():
    if not os.path.exists(OUTPUT_FILE):
        raise HTTPException(status_code=404, detail="Output insights not found")
    with open(OUTPUT_FILE, "r") as f:
        return json.load(f)

@app.post("/api/update")
async def update_data(payload: dict):
    try:
        # 1. Update the input file
        with open(INPUT_FILE, "w") as f:
            json.dump(payload, f, indent=4)
        
        # 2. Run the ML pipeline
        # We use subprocess to run the existing main.py which processes the data
        print(f"Triggering ML Pipeline at {time.ctime()}...")
        result = subprocess.run(["python", "main.py"], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error in ML Pipeline: {result.stderr}")
            return {"status": "error", "message": result.stderr}
        
        print("ML Pipeline completed successfully.")
        
        # 3. Read and return the new output
        if os.path.exists(OUTPUT_FILE):
            with open(OUTPUT_FILE, "r") as f:
                new_output = json.load(f)
            return {"status": "success", "output": new_output}
        else:
             return {"status": "success", "message": "Pipeline ran but output file not found yet."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

import threading

def watch_input_file():
    last_mtime = 0
    if os.path.exists(INPUT_FILE):
        last_mtime = os.path.getmtime(INPUT_FILE)
    
    print(f"File watcher started on {INPUT_FILE}")
    while True:
        try:
            if os.path.exists(INPUT_FILE):
                current_mtime = os.path.getmtime(INPUT_FILE)
                if current_mtime > last_mtime:
                    print(f"\n[Watcher] Detected change in {INPUT_FILE}. Triggering ML Pipeline...")
                    result = subprocess.run(["python", "main.py"], capture_output=True, text=True)
                    if result.returncode == 0:
                        print(f"[Watcher] ML Pipeline completed successfully at {time.ctime()}.")
                    else:
                        print(f"[Watcher] ML Pipeline Error: {result.stderr}")
                    last_mtime = current_mtime
        except Exception as e:
            print(f"Watcher error: {e}")
        time.sleep(2) # Check every 2 seconds

if __name__ == "__main__":
    watcher_thread = threading.Thread(target=watch_input_file, daemon=True)
    watcher_thread.start()
    uvicorn.run(app, host="0.0.0.0", port=8000)
