# How to setup
- After cloning, open your terminal and cd to this directory
- Create a python virtualenv: `pyenv virtualenv 3.11.3 subscription_env`
- Activate the virtualenv: `pyenv activate subscription_env`
- Install dependencies: `pip install -r requirements.txt`

# How to run the Flask App
- In the same terminal, run this command: `python myapp.py`
- You should see this message:
```python
* Serving Flask app 'myapp'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://localhost:8888
Press CTRL+C to quit
```
- Open your browser, and type this url in the address bar: `http://localhost:8888`
- Congrats! Flask app is up and running

# How to Test?
- Simply run the command: `pytest tests/`

# Sample commands using cURL
- Insert a user, product, product offer, and subscription
```
curl -X POST -d '{"username":"fudgeebar"}' -H "Content-Type: application/json" http://localhost:8888/api/v1/users
curl -X POST -d '{"name":"spotify"}' -H "Content-Type: application/json" http://localhost:8888/api/v1/products
curl -X POST -d '{"product_id":1,"price":149,"subscription_frequency":"monthly"}' -H "Content-Type: application/json" http://localhost:8888/api/v1/offers
curl -X POST -d '{"linked_account":1,"subscribed_product":1,"product_offer":1}' -H "Content-Type: application/json" http://localhost:8888/api/v1/subscriptions                                            
```
- Delete a subscription (unsubscribe)
```
curl -X DELETE http://localhost:8888/api/v1/subscriptions/1
```
- Renew a subscription
```
curl -X PUT http://localhost:8888/api/v1/subscriptions/1
```

### For the list of available APIs, please see `endpoints.py` 


