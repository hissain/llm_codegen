mkdir sample_project
cd sample_project
echo "streamlit" > requirements.txt
echo "import streamlit as st\n\nst.title(\"Hello World App\")\nst.write(\"Hello World\")\n\nuser_input = st.sidebar.text_input(\"Enter some text:\")\nif user_input:\n    st.write(f\"You entered: {user_input}\")" > app.py


pip install -r requirements.txt
streamlit run app.py