# ratestask

## To install dependencies

`pip install requirements/dev.txt`

## To start server

`python manage.py runserver`

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

