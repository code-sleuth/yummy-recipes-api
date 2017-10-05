[![Coverage Status](https://coveralls.io/repos/github/code-sleuth/yummy-recipes-api/badge.svg?branch=dev&cacheBuster=1)](https://coveralls.io/github/code-sleuth/yummy-recipes-api?branch=dev)
[![Build Status](https://travis-ci.org/code-sleuth/yummy-recipes-api.svg?branch=dev&cacheBuster=1)](https://travis-ci.org/code-sleuth/yummy-recipes-api)
[![Code Climate](https://codeclimate.com/github/code-sleuth/yummy-recipes-api/badges/gpa.svg)](https://codeclimate.com/github/code-sleuth/yummy-recipes-api)

# **Yummy Recipes API**
A RESTful API for yummy recipes

## Project Dependencies
1. Python 3.6.*
2. Postgresql 9.6.*
3. Flask 0.12.*

## Start application
1. Clone the repository to your computer

    ```
    git clone https://github.com/code-sleuth/yummy-recipes-api.git
    ```
    
2. In current clone directory, Create your virtual environment and start it.
   
   Linux and mac
    ```
    virtualenv <envname>
    ```
    For windows users:
    ```
    python -m venv env

    env\Scripts\activate
    ``` 

3. Install the packages in requirements.txt

    ``` 
    pip install -r requirements.txt 
    ```
4. Run the api

    ```
     $: python main_app.py
    ```
    
    api runs on port 5005
    
5. Use postman to navigate the endpoints in the api.

### Endpoints

-  Register new user

    ```
    /auth/register
    ``` 

    ```
    {
        "username": "username_without_spaces",
        "fullname": "Full Name",
        "password": "Pass"
    }
    ```
    
-  Login

    ```
    /auth/login
    ``` 
    Methods = ['POST']
        
    ```
    {
        "username": "user_name_here",
        "password": "pass"
    }
    ```
    
- Fetch All Users

    ```
    /users/
    ``` 
    Methods = ['GET']
        
- Edit user details

    ```
    /users/<int:id>
    ``` 
    Methods = ['GET', 'PUT', 'DELETE']
    
        ```
        /users/1
        ``` 
        
        Update username:
        ```
            {
                "username": "new_user_name"
            }
        ```
       


* #### Author
    ***Ibrahim Mbaziira***
