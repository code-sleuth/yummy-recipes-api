from app import set_app

# create an object pp
app = set_app()

if __name__ == '__main__':
    app.run(debug=True, port=5005)
