# Part 4: User Interface and Web Analytics

This final part of the project contains all the necessary files to run the Ukraine War Tweet Search Engine. This project is built on top of the already existing [skeleton](https://github.com/irwa-labs/search-engine-web-app). Some of the info in this README is thus the same as there.

## Starting the Web App

We will run the project using Python 3. Use the following command to execute the app.
```bash
python -V
# Make sure we use Python 3

cd search-engine-web-app
python web_app.py
```

Once the server starts running, you can open the Web App in your Browser:
[http://127.0.0.1:8088/](http://127.0.0.1:8088/) or [http://localhost:8088/](http://localhost:8088/)

This will open the Home page of the project. From here you can:

- Search information using the Search bar and the different algorithms. The used algorithm can be chosen by interacting with the dropdown list. The available algorithms are:
	- **Normal tf-idf**: Standard tf-idf vectors + cosine similarity
	- **Word2vec**: Tweets are converted to vectors in the Word2vec embedding space and compared with cosine similarity
	- **Likes tf-idf**: Same as Normal tf-idf, but taking into account the number of likes in the ranking
	- **Retweet tf-idf**: Same as Normal tf-idf, but taking into account the number of retweets in the ranking

You can also access the other functionalities from the top bar:
- Look in the **Dashboard** the information stored while researching
- Review different kind of user information in the **Stats** section
- Use the sentiment analysis system in the **Sentiment** section

## Virtualenv for the project (first time use)
### Install virtualenv
Having different version of libraries for different projects.  
Solves the elevated privilege issue as virtualenv allows you to install with user permission.

In the project root directory execute:
```bash
pip3 install virtualenv
virtualenv --version
```

### Prepare virtualenv for the project
In the root of the project folder run:
```bash
virtualenv .
```

If you list the contents of the project root directory, you will see that it has created several sub-directories, including a bin folder (Scripts on Windows) that contains copies of both Python and pip. Also, a lib folder will be created by this action.

The next step is to activate your new virtualenv for the project:

```bash
source bin/activate
```

or for Windows...
```cmd
myvenv\Scripts\activate.bat
```

This will load the python virtualenv for the project.

### Installing all the required packages
```bash
pip install -r requirements.txt
```




