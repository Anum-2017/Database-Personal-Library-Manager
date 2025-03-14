import sqlite3
from tabulate import tabulate

def display_library_table():
    try:
        # Connect to database
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        
        # Get all books
        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()
        
        if not books:
            print("Your library is empty! 📭")
            return
            
        # Create headers and convert read_status to emoji
        headers = ["Title", "Author", "Year", "Genre", "Read Status"]
        table_data = []
        
        for book in books:
            status = "✅ Read" if book[4] else "❌ Unread"
            table_data.append([
                book[0],  # Title
                book[1],  # Author
                book[2],  # Year
                book[3],  # Genre
                status
            ])
        
        # Display table
        print("\n📚 Personal Library Collection\n")
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print(f"\nTotal books: {len(books)} 📖")
        
    except sqlite3.OperationalError:
        print("⚠️ Error: Database not initialized! Run your Streamlit app first.")
    finally:
        conn.close()

if __name__ == "__main__":
    display_library_table()