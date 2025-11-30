from flask import Flask, render_template, request, redirect, url_for, session
import wikipedia

app = Flask(__name__)
# This Flask app sets app.secret_key, which is an encryption key used "to sign cookies and other things".
# Our app will work without it, but not completely. Without the secret key, we receive an error when searching:
# RuntimeError: The session is unavailable because no secret key was set.
# Storing secrets in plain code like this is not good practice. We know it.
# We don't want you to think we're endorsing this practice!
app.secret_key = 'IT@JCUA0Zr98j/3yXa R~XHH!jmN]LWX/,?RT'


@app.route('/')
def home():
    """Home page route."""
    return render_template("home.html")


@app.route('/about')
def about():
    """About page route."""
    return render_template("about.html")


@app.route('/search', methods=['POST', 'GET'])
def search():
    """Search page route. Return either form page to search, or search results."""
    if request.method == 'POST':
        session['search_term'] = request.form['search']
        return redirect(url_for('results'))
    return render_template("search.html")


@app.route('/results')
def results():
    """Results page route. Render the search results."""
    search_term = session['search_term']
    search_results = get_page(search_term)
    page, error_message, disambiguation_options = get_page(search_term)

    return render_template("results.html", page=page, error_message=error_message,
                           disambiguation=disambiguation_options, search_term=search_term)


def get_page(search_term):
    """Get a Wikipedia page object based on the search term."""
    # This function is not a route
    try:
        page = wikipedia.page(search_term, auto_suggest=False)
        return page, None, None
    except wikipedia.exceptions.PageError:
        # No such page, so return search error message
        error_message = f'Page id "{search_term}" does not match any pages. Try another id!'
        return None, error_message, None

    except wikipedia.exceptions.DisambiguationError as e:
        # This is a disambiguation page; return a list of possible pages
        return None, None, e.options


if __name__ == '__main__':
    app.run()
