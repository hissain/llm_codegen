import streamlit as st\n\nst.title("Hello World App")\nst.write("Hello World")\n\nuser_input = st.sidebar.text_input("Enter some text:")\nif user_input:\n    st.write(f"You entered: {user_input}")
