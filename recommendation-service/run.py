from app import app
if __name__ == '__main__':
    from waitress import serve
    #app.run(host="0.0.0.0", port=8082, debug=True)
    serve(app, host="0.0.0.0", port=8083, backlog=2048)