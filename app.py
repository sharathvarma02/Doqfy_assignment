from flask import Flask, request, render_template, jsonify, url_for

app = Flask(__name__)

# In-memory store for snippets
snippets = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create():
    text = request.form['text']
    password = request.form.get('password', None)  # Optional password

    # Create a snippet ID and store the snippet
    snippet_id = len(snippets) + 1
    snippets[snippet_id] = {'text': text, 'password': password}
    
    # Generate a URL for the snippet
    snippet_url = url_for('view', snippet_id=snippet_id, _external=True)
    return jsonify({'url': snippet_url})

@app.route('/view/<int:snippet_id>', methods=['GET', 'POST'])
def view(snippet_id):
    snippet = snippets.get(snippet_id)
    if snippet is None:
        return "Snippet not found", 404
    
    # Handle password protection
    if snippet['password']:
        if request.method == 'POST':
            input_password = request.form.get('password')
            if input_password == snippet['password']:
                return render_template('view.html', text=snippet['text'])
            else:
                return "Invalid password", 403
        return render_template('view.html', requires_password=True)
    else:
        return render_template('view.html', text=snippet['text'], requires_password=False)

if __name__ == '__main__':
    app.run(debug=True)
