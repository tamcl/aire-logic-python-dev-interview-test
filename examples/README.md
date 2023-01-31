Here are some examples:

Add users
```commandline
curl --location --request POST 'http://0.0.0.0:80/user/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "example_user1",
    "email": "user1@example.com"
}'
```

Change username
```commandline
curl --location --request POST 'http://0.0.0.0:80/user/update/?newUsername=example_user1_updated' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "example_user1",
    "email": "user1@example.com"
}'
```

Get user details
```commandline
curl --location --request GET 'http://0.0.0.0:80/user/?username=example_user1_updated'
```

Get list of bugs
```commandline
curl --location --request GET 'http://0.0.0.0:80/bug/list/?status=any'
```

Get a bug
```commandline
curl --location --request GET 'http://0.0.0.0:80/bug/?bugid=c50a601e-a34d-429f-b1be-ec5f7c85fadb'
```

Create a bug
```commandline
curl --location --request POST 'http://0.0.0.0:80/bug/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "title":"place bug title here",
    "description":"place bug description in here",
    "createdBy": "place a legit user id using get user"
}'
```

Assign a bug

We are assigning the bug to user 
```commandline
curl --location --request POST 'http://0.0.0.0:80/bug/assign/?userid=65db70f0-6657-40ec-8650-bfc194ca88a8&bugid=19a3edb6-e684-4568-a69e-a1e79a41ef9b'
```

Close a bug
```commandline
curl --location --request POST 'http://0.0.0.0:80/bug/close/?bugid=19a3edb6-e684-4568-a69e-a1e79a41ef9b'
```