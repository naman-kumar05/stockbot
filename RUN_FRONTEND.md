# 🚀 Running the Frontend

## Quick Start

From the project root directory:

```bash
cd ui
python -m streamlit run app.py
```

Or use the batch file:
```bash
start_frontend.bat
```

## Alternative Methods

### Method 1: Using Python Module (Recommended)
```bash
cd ui
python -m streamlit run app.py
```

### Method 2: If streamlit is in PATH
```bash
cd ui
streamlit run app.py
```

### Method 3: Direct Python Execution
```bash
cd ui
python -c "import streamlit.web.cli as stcli; stcli.main()" run app.py
```

## Troubleshooting

### Issue: 'streamlit' is not recognized
**Solution:** Use `python -m streamlit` instead:
```bash
python -m streamlit run app.py
```

### Issue: Module not found
**Solution:** Install streamlit:
```bash
pip install streamlit
```

### Issue: Port already in use
**Solution:** Use a different port:
```bash
python -m streamlit run app.py --server.port 8502
```

## Full Startup Sequence

1. **Start Backend** (Terminal 1):
   ```bash
   uvicorn api.main:app --reload --port 8000
   ```

2. **Start Frontend** (Terminal 2):
   ```bash
   cd ui
   python -m streamlit run app.py
   ```

3. **Open Browser:**
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000/docs
