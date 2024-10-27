from flask import Flask, render_template, request
import numpy as np
import pickle

# Load the data
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html', 
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num-rating'].values),
                           rating=list(popular_df['avg_rating'].values))

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input').strip().lower()  # Normalize user input
    matched_books = [book for book in pt.index if user_input in book.lower()]  # Find matches

    if not matched_books:
        return render_template('recommend.html', error="Sorry, no books found matching your input.", matched_books=[])

    # If there's more than one match, you can choose the first one or implement a suggestion mechanism
    book_title = matched_books[0]
    index = np.where(pt.index == book_title)[0][0]

    similar_items = list(enumerate(similarity_scores[index]))
    similar_items.sort(key=lambda x: x[1], reverse=True)
    similar_items = similar_items[1:6]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)

    return render_template('recommend.html', data=data, matched_books=matched_books)

if __name__ == '__main__':
    app.run(debug=True)
