from flask import Flask, render_template, send_from_directory, url_for
import os.path

app = Flask(__name__)


# Public facing pages.
@app.route("/")
def index():
    return render_template('index.html')


# Start the application.
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001, ssl_context=("ssl/local.crt", "ssl/local.key"))