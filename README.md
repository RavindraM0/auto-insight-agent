# Auto-Insight Agent Pro (Streamlit-ready)
Ready-to-deploy Streamlit project that includes a local Flan-T5 based NL->SQL translator.

## Quick start (local)
1. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the app:
   ```
   streamlit run app.py
   ```

## Deploy to Streamlit Community Cloud
1. Push this repository to GitHub (make sure `app.py` is at the repo root).
2. Go to https://streamlit.io/cloud -> New app -> select this repo, branch main, main file `app.py`.
3. Deploy.

## Notes
- First-time run will download the Flan-T5 model (~400-800MB). Keep this in mind for Streamlit Cloud (it will cache).
- If Streamlit Cloud fails due to model size, consider switching to a smaller model like `google/flan-t5-small` in `agents/query_agent.py`.
