Instructions for local deploy:
1. Create new venv 
2. ```pip install -r requirements.txt```
3. ```docker run -d -p 6379:6379 redis```
4. ```python manage.py makemigrations```
5. ```python manage.py migrate```
6. ```python manage.py runserver```
7. ```python manage.py createsuperuser```
8. Go to the admin panel and make a few questions in the answers
9. ```tests/``` - all available tests
10. Go to the ```tests/slug_for_test_you_want_to_take/```
11. Go to the ```tests/slug_test_you_want_to_take/save-answer/```
12. Make a **PATCH** request with a request body:
```json
{
  "question": "<question id>",
  "answer": "<answer id>"
}
```
13. Answer all quiz questions
14. Go to the ```tests/slug_for_test_you_want_to_take/submit/``` and make **POST** request and get the test result. The test result has already been sent to your email.