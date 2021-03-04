# ratestask

**Steps**

1. Create a `Python 3.7` virtualenv and activate it.
2. Clone the repository -: `git clone https://github.com/pygaur/ratestask.git`
3. `cd` to App -: `cd ratestask/ratestask`
5. Install dependencies :- `pip install requirements/dev.txt`
6. create database in postgres.
7. migrate your models - `python manage.py migrate`
8. run server `python manage.py runserver`


## Total time spent

`10-12 hrs`

## Batch Processing Task

Each time my API will receive request to update price, I will publish a message to a message broker(rabbitmq).

I will write consumers which will be processing these **rabbitmq** messages.

With above approach i am providing -
1. Processing price update in background (we can make it super scale)
2. setting up retry queues(we will retry if any error comes in processing)
3. I can use multi processing( run more than 1 consumer in parallel) to process heavy data.
4. system will be highly decoupled

**Tech Stack** :- Flask , celery , rabbitmq , postgres, redis. 

![image](https://user-images.githubusercontent.com/43163597/109892088-4e057180-7cb0-11eb-999c-92783cf9f370.png)



**NOTE**

Have not written unit test cases for this app due to time constraint. 
