# tokenpool

#default port is 8000


ENDPOINTS
1.for creating random token in pool
GET http://localhost:8000/create_token/

2.for keep alive token for 5 minutes 
GET http://127.0.0.1:8000/keep_alive/<int:token>/


3.for assign token
GET http://127.0.0.1:8000/assign_token/


4.for unblocking token 
GET http://127.0.0.1:8000/unblock_token/<int:token>/
