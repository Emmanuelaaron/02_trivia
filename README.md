# Trivia
## Getting Started
### Prerequisites and local storage
Developers contributing to this product should have the following installed on their local machines
- python3
- pip 
- node
- virtualenv

#### Backend
- cd into the backend directory <br/>
`$ cd backend`
- create a virtual environment and activate it using the command below <br/>
`$ virtualenv venv ` <br/>
`$ source venv/Scripts/activate`
- Install all the dependencies within the requirements file using the command below <br />
`$ pip install -r requirements.txt`
- To Run the application use the following commands <br />
`$ export FLASK_APP=flaskr`
`$ export FLASK_ENV=development`
`$ flask run`
By default the applucation is run on http://127.0.0.1:5000/
* copy the Url it into postman and put to run any endpoint of your preference in the table below 

HTTP Method | Endpoint | Functionality | Parameters 
------------|----------|---------------|------------
GET | / | Getting all available categories | None
GET | /questions | Getting all questions | None
DELETE | /questions/question_id |Deletes a question using an id | question_id
POST | /questions| Creates a question| None
POST | /questions/search | Getting questions basing on a search term | None
GET | /categories/category_id/questions | Getting questions based on category | category_id

To post a question, the data should be in this format
```
{
	"question": "question",
	"answer": "answer",
	"category": category,
	"difficulty": category
}
``` 
<br />
To search for a question, the data should be in this format. <br />
`
{
	"question": search_word
}
`

### Frontend
- cd into the frontend directory <br />
`$ cd frontend`
- Install all the dependencies using the command below
`$ npm install`
- Then run the server using the command below
`$ npm start`

### Authors
Emmanuel Isabirye



