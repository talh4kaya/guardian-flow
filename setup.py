import os

# Klasör yapısı
directories = [
    "data/raw",
    "data/processed",
    "data/drift_db",
    "docs",
    "models",
    "notebooks",
    "src/data",
    "src/features",
    "src/models",
    "src/monitoring",
    "src/api",
    "tests",
    ".github/workflows",
]

# Dosyalar ve içerikleri
files = {
    ".gitignore": """
__pycache__/
*.py[cod]
venv/
.env
data/
!data/.gitkeep
.vscode/
*.pkl
*.joblib
""",
    "requirements.txt": """
pandas
numpy
scikit-learn
matplotlib
seaborn
jupyterlab
pytest
fastapi
uvicorn
pydantic
python-dotenv
pre-commit
""",
    "README.md": "# Guardian-Flow\nReal-time Fraud Detection System Project",
    "src/__init__.py": "",
    "src/api/main.py": "",
    "data/raw/.gitkeep": "",
    "data/processed/.gitkeep": "",
    "data/drift_db/.gitkeep": "",
}


def create_structure():
    # Klasörleri oluştur
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Klasör oluşturuldu: {directory}")

    # Dosyaları oluştur
    for filepath, content in files.items():
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content.strip())
        print(f"Dosya oluşturuldu: {filepath}")


if __name__ == "__main__":
    create_structure()
