# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## ToDo Tasks
These are the files you'd want to edit in the backend:

1. *./backend/flaskr/`__init__.py`*
2. *./backend/test_flaskr.py*


One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 


2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 


3. Create an endpoint to handle GET requests for all available categories. 


4. Create an endpoint to DELETE question using a question ID. 


5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 


6. Create a POST endpoint to get questions based on category. 


7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 


8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 


9. Create error handlers for all expected errors including 400, 404, 422 and 500. 



## API Documentation
### Getting Started
This project is not currently hosted anywhere, hence the server is locally run and served. 

* Base URL: ```http://127.0.0.1:5000```
* Authentication: None

### Endpoints

#### *GET '/api/v1.0/categories'*

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 

e.g. `curl -X GET /api/v1.0/categories`

```
    {
        '1' : "Science",
        '2' : "Art",
        '3' : "Geography",
        '4' : "History",
        '5' : "Entertainment",
        '6' : "Sports"
    }
```

#### *GET '/api/v1.0/categories/<cat_id>'*

- Fetches a single category object based on the id passed in endpoint
- Endpoint Parameters: `cat_id` which represents a category ID
- Request Arguments: None
- Returns: A single *Category* object composed of ID and type

e.g. `curl -X GET /api/v1.0/categories/5`

```
    {
        '5': 'Entertainment'
    } 
```
- Errors: 404 error returned when category id is missing from database

#### *GET '/api/v1.0/questions?page={number}'*

- Fetches a dictionary of questions in which the keys are:
    - `questions`: The value for which is a paginated list of *Question* objects
    - `totalQuestions`: This maps to the total question count in the database
    - `categories`: The dictionary representing *Category* objects
- Request Arguments: 
    - `page`: An integer value representing the page number
- Returns: An object having the questions, categories and total question count

e.g. `curl -X GET /api/v1.0/questions?page=2`
```
    {
        'questions': [
            {
                'id': 1,
                'question': 'This is a question',
                'answer': 'This is an answer', 
                'difficulty': 5,
                'category': 2
            },
        ],
        'totalQuestions': 100,
        'categories': { '1' : "Science",
        '2' : "Art",
        '3' : "Geography",
        '4' : "History",
        '5' : "Entertainment",
        '6' : "Sports" },
    }
```
- Errors: 404 error returned when page number is less than 0 or exceeds total

#### *GET '/api/v1.0/categories/{category_id}/questions'* 

- Fetches a dictionary of questions in which the keys are:
    - `questions`: The value for which is a list of *Question* objects for the given `category_id`
    - `totalQuestions`: This maps to the total question count in the database
    - `currentCategory`: The current category string
- Endpoint Parameters: `category_id` is integer ID for a certain category
- Returns: An object having the questions, categories and total question count

e.g. `curl -X GET /api/v1.0/categories/1/questions`
```
    {
        'questions': [
            {
                'id': 1,
                'question': 'This is a question',
                'answer': 'This is an answer', 
                'difficulty': 5,
                'category': 4
            },
        ],
        'totalQuestions': 100,
        'currentCategory': 'Science'
    }
```
- Errors: 404 error returned when category ID does not exist

#### *POST '/api/v1.0/questions'*

There are two variants for this API endpoint:

1. Adding a new question:
    - Fetches a dictionary of keys representing success state and a message
    - Request Arguments: A single object composed of following keys and associated values - `question`, `answer`, `difficulty` and `category`
    - Returns: An object representing success state and message

    e.g. `curl -X POST /api/v1.0/questions -d '{"question": "What is the smallest prime ?", "answer": "2", "difficulty": "1", "category": "1"}'`

    ```
        {
            "success": true,
            "message": "Added successfully"
        }
    ```
    - Errors: A 500 error in case server fails to add a new question and a 400 in case the request is formatted wrongly

2. Searching for a question:
    - Fetches a response dictionary of keys having questions and total question count
    - Request Arguments: A key called `searchTerm` with a corresponding search string requested by a user
    - Returns: An object containing all questions which match the query string along with the total count

    e.g. `curl -X POST /api/v1.0/questions -d '{"searchTerm": "A Game of"}'`

    ```
        {
            "questions": [
                {
                    "id": 2,
                    "question": "Which author wrote 'A Game of Thrones'?",
                    "answer": "George RR Martin",
                    "difficulty": 2,
                    "category": 5
                }
            ],
            "totalQuestions": 15
        }
    ```

#### *POST '/api/v1.0/quizzes'*

- Fetches a single `Question` object randomly picked from a list of questions from a specific category exclusive from a set of previous questions
- Request Arguments: `previous_questions` which represents an array of previous question IDs and `quiz_category` which is a string that represents the choice of category
- Returns: A single question object 

e.g. `curl -X POST http://localhost:5000/api/v1.0/quizzes -d '{"previous_questions": [2,3,4], "current_category": "Entertainment"}'`

```
    {
        'question': {
            'id': 11,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 3,
            'category': 5
        }
    }
```

#### *DELETE '/api/v1.0/questions/{question_id}'* 

- Fetches a dictionary whose keys represent status code and id of the question that was deleted
- Endpoint Parameters: `question_id` is integer ID for a question
- Returns: An object having status code and id

e.g. `curl -X DELETE /api/v1.0/questions/22`

```
    {
        'statusCode': 200,
        'id': 22
    }
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
