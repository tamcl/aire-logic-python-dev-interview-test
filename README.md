Arie Logic's python dev interview test

Your goal is to implement a simple bug tracker. The features we would like, in no particular order:

- [ ] It should be possible to view the list of open bugs, including their titles
- [ ] It should be possible to view the detail of individual bugs, including the title the full description, and when it was opened
- [ ] It should be possible to create bugs
- [ ] It should be possible to close bugs
- [ ] It should be possible to assign bugs to people
- [ ] It should be possible to add people to the system
- [ ] It should be possible to change people's names
- [ ] The web application should look nice
- [ ] The web application should expose some sort of API
- [ ] The data should be stored in some sort of database

There are 6 key areas that the dev marking your test will look at, they are:
 - Documentation
 - Setup
 - Functionality
 - Usability
 - Project Structure
 - Testing

---
This code runs in 3.9
```commandline
pip install -r requirements.txt
```

Activate api
```commandline
uvicorn src.api.api:app --host 0.0.0.0 --port 80
```

Run test unit
```commandline
python test.py
```

Open Client
```commandline
--
```