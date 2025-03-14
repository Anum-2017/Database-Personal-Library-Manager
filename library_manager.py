import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="📚 Personal Library Manager", page_icon="📖", layout="wide")

# Database initialization
def initialize_database():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS books (
            title TEXT,
            author TEXT,
            year INTEGER,
            genre TEXT,
            read_status INTEGER
        )
    ''')
    conn.commit()
    conn.close()

initialize_database()

# Custom CSS styles
st.markdown(
    """
    <style>
    /* Main app background - Pure black */
    .stApp {
        background-color: #000000;
        color: white;
    }

    /* Sidebar background - Dark gray */
    section[data-testid="stSidebar"] {
        background-color: #222222;
    }

    /* Styling for text elements */
    h1, h2, h3, h4, h5, h6, p, span, label {
        color: white !important;
    }

    /* Input fields and buttons */
    .stTextInput, .stNumberInput, .stSelectbox, .stRadio {
        color: white !important;
    }

    .stButton>button {
        color: white !important;
        background-color: #333333 !important;
        border: 1px solid #555555 !important;
    }

    .stButton>button:hover {
        background-color: #444444 !important;
        border-color: #777777 !important;
    }

    .stProgress > div > div {
        background-color: #1db954 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# App header
st.markdown("<h1 style='text-align: center;'>📚 Personal Library Manager</h1>", unsafe_allow_html=True)

# Sidebar configuration
try:
    st.sidebar.image("icon.png", use_container_width=True)
except:
    st.sidebar.write("⚠️ Image not found: 'icon.png'")

menu_options = {
    "Homepage": "🏠 Homepage",
    "Add a New book": "📚 Add a book",
    "Remove a book": "🗑️ Remove a book",
    "Search for a book": "🔍 Search for a book",
    "Display all books": "📖 Display all books",
    "Display statistics": "📊 Display statistics",
}

menu = st.sidebar.selectbox("Choose an option", list(menu_options.values()))

# Homepage
if menu == menu_options["Homepage"]:
    st.markdown("<h3 style='text-align: center;'>Welcome to Your Personal Library Manager! 📚</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>This app allows you to manage your book collection, track your reading progress, and keep everything organized.</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Use the sidebar to add, remove, search, or view books. You can also check out your reading stats!</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Enjoy your reading journey! 😄</p>", unsafe_allow_html=True)
    try:
        st.image("homepage.jpg", use_container_width=True)
    except:
        st.warning("⚠️ Image not found: 'homepage.jpg'")

# Add Book
elif menu == menu_options["Add a New book"]:
    st.subheader("📝 Add a New Book")
    title = st.text_input("**📚 Enter the book title**")
    author = st.text_input("**✍️ Enter the author**")
    year = st.number_input("**📅 Enter the publication year**", min_value=1, max_value=2025, value=2023)
    genre = st.text_input("**📚 Enter the genre**")
    read_status = st.radio("**🤔 Have you read this book?**", ("Yes ✅", "No ❌"))
    
    if st.button("Add Book ➕"):
        if title and author and genre:
            conn = sqlite3.connect('library.db')
            c = conn.cursor()
            c.execute("INSERT INTO books VALUES (?, ?, ?, ?, ?)",
                     (title, author, year, genre, 1 if read_status == "Yes ✅" else 0))
            conn.commit()
            conn.close()
            st.success(f"📘 Book '{title}' added successfully!")
        else:
            st.warning("⚠️ Please fill in all fields to add the book.")

# Remove Book
elif menu == menu_options["Remove a book"]:
    st.subheader("🗑️ Remove a Book")
    title_to_remove = st.text_input("**📚 Enter the title of the book to remove**")
    
    if st.button("Remove Book 🗑️"):
        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute("DELETE FROM books WHERE LOWER(title) = LOWER(?)", (title_to_remove,))
        conn.commit()
        if conn.total_changes > 0:
            st.success(f"📖 Book '{title_to_remove}' removed successfully!")
        else:
            st.warning(f"⚠️ Book with title '{title_to_remove}' not found.")
        conn.close()

# Search Books
elif menu == menu_options["Search for a book"]:
    st.subheader("🔍 Search for a Book")
    search_by = st.selectbox("**Search by**📜", ["Title", "Author"])
    search_query = st.text_input(f"**Enter the {search_by.lower()}🧐** ")
    
    if st.button("Search 🔎"):
        conn = sqlite3.connect('library.db')
        if search_by == "Title":
            results = pd.read_sql("SELECT * FROM books WHERE LOWER(title) LIKE LOWER(?)", 
                                conn, params=('%'+search_query+'%',))
        else:
            results = pd.read_sql("SELECT * FROM books WHERE LOWER(author) LIKE LOWER(?)", 
                                conn, params=('%'+search_query+'%',))
        conn.close()
        
        if not results.empty:
            results['Read Status'] = results['read_status'].map({1: 'Read ✔️', 0: 'Unread ❌'})
            st.dataframe(results[['title', 'author', 'year', 'genre', 'Read Status']]
                        .rename(columns={'title': 'Title', 'author': 'Author', 
                                        'year': 'Year', 'genre': 'Genre'}))
        else:
            st.warning("⚠️ No books found.")

# Display All Books
# In your "Display all books" section
elif menu == menu_options["Display all books"]:
    st.subheader("📚 All Books in Your Library")
    
    try:
        conn = sqlite3.connect('library.db')
        books_df = pd.read_sql("SELECT * FROM books", conn)
        
        if not books_df.empty:
            books_df['Read Status'] = books_df['read_status'].map({1: '✔️ Read', 0: '❌ Unread'})
            display_df = books_df[['title', 'author', 'year', 'genre', 'Read Status']]
            display_df.columns = ["Title", "Author", "Year", "Genre", "Status"]
            st.dataframe(display_df)
        else:
            st.warning("⚠️ Your library is empty.")
            
    except sqlite3.OperationalError as e:
        st.error(f"Database error: {str(e)}")
        st.info("Please add at least one book first!")
    finally:
        conn.close()

# Statistics
elif menu == menu_options["Display statistics"]:
    st.subheader("📊 Library Statistics")
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM books")
    total_books = c.fetchone()[0]
    
    if total_books > 0:
        c.execute("SELECT COUNT(*) FROM books WHERE read_status = 1")
        read_books = c.fetchone()[0]
        percentage_read = (read_books / total_books) * 100
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"📚 Total books: <br><span style='font-size: 40px;'>{total_books}</span>", 
                       unsafe_allow_html=True)
        with col2:
            st.markdown(f"✅ Percentage read: <br><span style='font-size: 40px;'>{percentage_read:.2f}%</span>", 
                       unsafe_allow_html=True)
        st.progress(percentage_read / 100)
    else:
        st.write("❌ No books to display statistics for.")
    conn.close()

# Footer
st.markdown(""" 
    <hr>
    <p style='text-align: center; font-size: 14px;'>Developed by Anum Kamal 💜 | Powered by Streamlit 🚀</p>
""", unsafe_allow_html=True)