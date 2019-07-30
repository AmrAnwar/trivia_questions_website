# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

- inside the backend directory 

```bash
export FLASK_APP=flaskr
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

## Website image
after adding the endpoints:
![trivia_questions_site](https://www7.0zz0.com/2019/07/30/20/439477930.jpeg)

## Endpoints

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- url params: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
```json
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}
```

### 

GET '/questions'
or
GET '/questions?page=2' 
- FETCH a list of question objects with pagination

- url params: page, default = 1
- RETURN a list of questions,
    number of total questions, current category, categories.
- Response:
```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "",
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 
                    'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    ... etc
     ],
  "success": true,
  "total_questions": 25
}
```

### 

POST '/questions' 
Content-Type: application/json

- ADD new question object
- url params: None
- json data:
```json
{
    "question": "1+1",
    "answer": "2",
    "difficulty": 1,
    "category": 1
}
```
- Response: 
```json
{
  "question": {
    "answer": "2",
    "category": 1,
    "difficulty": 1,
    "id": 36,
    "question": "1+1"
  },
  "success": true
}
```

###

POST  /questions
Content-Type: application/json

- SEARCH about questions with similar title 
- url params: None
- json data:
```json
{
    "searchTerm": "what is"
}
```
- Response: 
```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "",
  "questions": [
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```
###

DELETE /questions/<id>

- DELETE question by id 
- url params: id
- Response: 


```json
url: DELETE http://127.0.0.1:5000/questions/22

{
  "delete": 22,
  "success": true
}
```
###

GET /categories/<id>/questions 

- FETCH questions list based on category
- url params: category id 
- Response:
```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "Art",
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    ... etc
  ],
  "success": true,
  "total_questions": 4
}
```

### 
GET /quizzes 
Content-Type: application/json

- RETURN return a random questions within the given category
- url param: None
- json data:
```json
{
    "previous_questions": [5],
    "quiz_category": {
        "type": "Science",
        "id": 4
    }
}
```
- RETURN a random questions within the given category
- Response:
```json
{
  "question": {
    "answer": "Muhammad Ali",
    "category": 4,
    "difficulty": 1,
    "id": 9,
    "question": "What boxer's original name is Cassius Clay?"
  },
  "success": true
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