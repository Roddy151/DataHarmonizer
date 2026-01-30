# 🧬 Data Harmonizer

**ETL Last Mile Assistant | Unify disparate data sources with ease.**

Data Harmonizer is a Streamlit-based application designed to streamline the "last mile" of ETL processes. It provides a user-friendly wizard interface to ingest, transform, and standardize messy Excel or CSV data into clean, structured formats ready for downstream systems.

## ✨ Features

- **Wizard-Driven Workflow**: A guided 4-step process to ensure data integrity.
    1.  **Ingest**: Upload your raw data files (Excel/CSV).
    2.  **Unify**: Detect and handle pivot tables or cross-tab formats.
    3.  **Curate**: Map columns to a target schema and validate types.
    4.  **Export**: Download the harmonized data in a standardized format.
- **Robust Data Handling**: Built on `pandas` and `pyarrow` for efficient processing.
- **Excel Support**: Native support for reading and writing Excel files using `openpyxl` and `xlsxwriter`.

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Data Processing**: [Pandas](https://pandas.pydata.org/), [PyArrow](https://arrow.apache.org/)
- **Excel Engine**: [OpenPyXL](https://openpyxl.readthedocs.io/), [XlsxWriter](https://xlsxwriter.readthedocs.io/)
- **Containerization**: Docker

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Pip (Python Package Manager)

### Installation

1.  **Clone the repository**
    ```bash
    git clone <repository_url>
    cd data_harmonizer
    ```

2.  **Create a virtual environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

### Usage

**Run locally:**
```bash
streamlit run app.py
```
Or use the provided helper script:
```bash
./run_app.sh
```

**Run with Docker:**
```bash
docker build -t data-harmonizer .
docker run -p 8501:8501 data-harmonizer
```
Access the app at `http://localhost:8501`.

## 📂 Project Structure

```
data_harmonizer/
├── core/               # Core business logic and data processing
├── ui/                 # Streamlit UI components and wizard steps
├── tests/              # Unit and integration tests
├── app.py              # Main application entry point
├── Dockerfile          # Docker configuration
├── requirements.txt    # Python dependencies
└── run_app.sh          # Execution helper script
```

## 📄 License

[MIT](LICENSE)
