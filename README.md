Arie Logic's python dev interview test

Your goal is to implement a simple bug tracker. The features we would like, in no particular order:

- [x] It should be possible to view the list of open bugs, including their titles
- [x] It should be possible to view the detail of individual bugs, including the title the full description, and when it was opened
- [x] It should be possible to create bugs
- [x] It should be possible to close bugs
- [x] It should be possible to assign bugs to people
- [x] It should be possible to add people to the system
- [x] It should be possible to change people's names
- [ ] The web application should look nice
- [x] The web application should expose some sort of API
- [x] The data should be stored in some sort of database

There are 6 key areas that the dev marking your test will look at, they are:
 - Documentation
 - Setup
 - Functionality
 - Usability
 - Project Structure
 - Testing

---
This code runs in Python 3.9
```commandline
pip install -r requirements.txt
```

Activate api (everything in the code is hardcoded for http://0.0.0.0:80/)
```commandline
uvicorn src.api.api:app --host 0.0.0.0 --port 80
```
After starting the server for the api

Please use http://0.0.0.0:80/docs to access the swagger doc

Run unit test (!!everytime it runs, it will reset the database!!)
```commandline
python test.py
```

Please refer to example directory to use command lines, there's a postman collection as a reference.