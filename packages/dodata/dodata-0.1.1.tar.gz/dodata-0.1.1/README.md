# DoData python library 0.1.1

## Installation

```
pip install "dodata[demos]"
```

## Setup

Create a `.env` file in your working directory.

```
dodata_url = 'https://your.dodata.url.here'
dodata_user = 'dodata_user'
dodata_password = 'dodata_web_password'
dodata_db = 'your.dodata.database.url.here'
dodata_db_user = "db_username_here"
dodata_db_password = "db_password_here"
dodata_db_name = "dodata"
data_db_port = 5432
debug = False
```

For standard python execution the `.py` file can be in the same directory as the `.env` file or in a parent directory.
