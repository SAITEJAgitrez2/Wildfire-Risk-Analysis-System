import os

# Define the project folder structure
folders = [
    "wildfire-risk-analysis/data/raw",
    "wildfire-risk-analysis/data/processed",
    "wildfire-risk-analysis/notebooks",
    "wildfire-risk-analysis/rapidminer",
    "wildfire-risk-analysis/models",
    "wildfire-risk-analysis/app/dashboard"
]

files = {
    "wildfire-risk-analysis/README.md": "# Wildfire Risk Analysis System\n\nProject using Python, RapidMiner, and ML models to predict and visualize wildfire risk.",
    "wildfire-risk-analysis/app/main.py": "# Entry point for the backend (Flask or FastAPI)\n\nif __name__ == '__main__':\n    print('Run your API server here')"
}

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create files with default content
for filepath, content in files.items():
    with open(filepath, "w") as f:
        f.write(content)

print("✅ Project structure created successfully.")
