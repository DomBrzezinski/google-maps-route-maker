from flask import Flask, render_template
import socketio
import eventlet
import routeFinder

app = Flask(__name__)

results = str(routeFinder.main())
print(results)


@app.route('/home')
def greeting():  
    # return render_template("index.html")
    return results

if __name__ == '__main__':
    app.run(port=3000)