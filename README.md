[![Coverage Status](https://coveralls.io/repos/github/code-sleuth/yummy-recipes-api/badge.svg?branch=dev&cacheBuster=1)](https://coveralls.io/github/code-sleuth/yummy-recipes-api?branch=dev)
[![Build Status](https://travis-ci.org/code-sleuth/yummy-recipes-api.svg?branch=dev&cacheBuster=1)](https://travis-ci.org/code-sleuth/yummy-recipes-api)
[![Maintainability](https://api.codeclimate.com/v1/badges/feffc843869abc06a0e7/maintainability)](https://codeclimate.com/github/code-sleuth/yummy-recipes-api/maintainability)

# **Yummy Recipes API**
A RESTful API for yummy recipes

## Project Dependencies
1. Python 3.6.*
2. Postgresql 9.6.*
3. Flask 0.12.*

[Project Hosted on Heroku](https://yummy-recipes-api-pro.herokuapp.com)

## How to run flask application
1. Create a folder <yummy-recipes> on your computer
   Clone repository to your computer into created folder

    ```
    git clone https://github.com/code-sleuth/yummy-recipes-api.git
    ```
2. Navigate into created folder

    ```
    cd yummy-recipes
    ```
3. Create and activate  virtual environment.

    ```
        $ virtualenv  venv

        $ source venv/bin/activate
    ```

    More on setting up Virtual environment: [how to set up virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/)

4. Install the packages in requirements.txt

    ``` pip install -r requirements.txt ```

5. Set up postgresql database and copy connection string for example.

    ``` DATABASE_URL='postgres://<db_user_name>:<password>@localhost/<database_name>' ```

    and

    ``` DATABASE_URL='postgres://<db_user_name>:<password>@localhost/<test_database_name>' ```

    How to setup postgresql: [how to setup postgresql mac](https://gist.github.com/sgnl/609557ebacd3378f3b72)

6. To start the api, using terminal, run the following commands

    ```export FLASK_APP='main_app.py'```

    ```export APP_SETTINGS='development'```

    ```export SECRET='i wont tell if you dont'```

    ```export DATABASE_URL='postgres://<db_user_name>:<password>@localhost/<database_name>'```

    ```export TEST_DB_URL='postgres://<db_user_name>:<password>@localhost/<test_database_name>```

    ```flask run ```
7. Using postman, the url to run the api locally is ```http://127.0.0.1:5000/```.

8. On the web, visit the url ```https://yummy-recipes-api-pro.herokuapp.com/swagger_docs/```

9. Using postman with web url ```https://yummy-recipes-api-pro.herokuapp.com/```

    
10.Sample: Use postman to navigate the endpoints in the api.

### Endpoints Example

-  Register new user
    Web url:
    ```
    https://yummy-recipes-api-pro.herokuapp.com/auth/register
    ``` 
    Locally:
    ```
    http://127.0.0.1:5000/auth/register
    ```

    ```
    {
        "username": "username",
        "fullname": "Full Name",
        "password": "Pass"
    }
    ```

- More on the end point is availabe online via the documentation
  ```
    https://yummy-recipes-api-pro.herokuapp.com/swagger_docs/
  ```
       

* #### Author
    ***Ibrahim Mbaziira***
