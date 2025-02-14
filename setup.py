from setuptools import setup, find_packages

setup(
    name="docai",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.104.1",
        "uvicorn==0.24.0",
        "python-multipart==0.0.18",
        "PyPDF2==3.0.1",
        "python-docx==0.8.11",
        "openpyxl==3.1.2",
        "Pillow==10.1.0",
        "pytesseract==0.3.10",
        "openai==1.3.0",
        "python-dotenv==1.0.0",
        "SQLAlchemy==2.0.23",
        "aiofiles==23.2.1",
        "pydantic==2.5.1",
        "pydantic-settings==2.1.0",
    ],
)
