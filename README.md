# NUWS-API-Version-1

![EmailScrapper](doc/hbnb-logo.png)

## Description :book:

The NUWS-API is a basic Extract-Transform-Load (ETL) data pipeline that extracts data from various field submissions, makes transforms to the data and loads it into a dedicated MYSQL server database. The field submissions are collected using a data collection tool called Kobo Toolbox. You can read more about Kobo Toolbox platform here: [KoboToolbox](https://kobotoolbox.org/#home). The data collected is extracted through an Application Programming Inteface (API) provided by the platform. The data further transformed in the backend of the application at mapped to its corresponding MYSQL tables.
The complete application on the backend is integrating a KoboToolbox Data collection API, an ETL data pipeline, a MySQL server database and Flask RESTful API with a dynamic landing page made from HTML5/CSS3 on the front-end.

![EmailScrapper](doc/hbnb-stack.png)

This repository contains the first version of the NUWS data pipeline API. You can check out this section for links to newer versions and features in these links below.

- [nuws-api-v1](https://github.com/lukwagoraymond/nuws-api-v1)

## Dependencies and Installation :couple:

There are two ways to test this Minimum Viable Application (MVP) out on your machine; (1) Clone this entire repository on your machine & test or (2) Simply run the docker container on your local machine.

### (1) Clone Entire repository on Machine & Test

- Clone this repo on your local machine and open the folder
- Once you're within the folder, run the following code below within in your console terminal to set up your virtual working environment. NB: Replace <virtual_wrk_env_name> with your desired name of the virtual working environment. Code below works for machines running on UNIX OS only.

```console
raymond@raymond-ThinkPad-T480:~/nuws-api-v1$ virtualenv <virtual_wrk_env_name>
....
```
NB: Ensure you have pip and virtualenv package installed on your machine.

```console
raymond@raymond-ThinkPad-T480:~/nuws-api-v1$ source <virtual_wrk_env_name>/bin/activate
....
```
- Once you have run the code blocks above successfully, your console should resemble something like this below.

```console
(<virtual_wrk_env_name>) raymond@raymond-ThinkPad-T480:~/nuws-api-v1$ 
....
```

- Run the requirements.txt file to install all the required dependencies for this application on your machine. Run this code below:

```console
raymond@raymond-ThinkPad-T480:~/nuws-api-v1$ pip install -r requirements.txt
....
```

Application:

| Tool/Library    | Version   |
| ------------    | -------   |
| Python          | 3.10.6    |
| MySQL           | 8.0.32    |
| Flask           | 2.2.3     |
| flasgger        | 0.9.5     |
| mysqlclient     | 2.1.1     |
| SQLAlchemy      | 2.0.7     |
| requests        | 2.28.2    |
| pandas          | 1.5.3     |
| attrs           | 22.2.0    |
| certifi         | 2022.12.7 |
| pyproject_hooks | 1.0.0     |
| python-dateutil | 2.8.2     |
| urllib3         | 1.26.15   |
| loguru          | 0.6.0     |
| colorlog        | 6.7.0     |

Deployment:

| Tool/Library | Version  |
| ------------ | -------  |
| docker       | 20.10.17 |

- Once you have all the previous dependencies installed in your machine you have to set up the MYSQL database.

- Go to "nuws-api-v1" folder and execute the lines of code below: NB: Set your own password in the sql script

```console
raymond@raymond-ThinkPad-T480:~/nuws-api-v1$ cat setup_mysql_db.sql | mysql -hlocalhost -uroot -p
Enter password:
raymond@raymond-ThinkPad-T480:~/nuws-api-v1$ echo "SHOW DATABASES;" | mysql -unuws_dev -p | grep nuws_data_db
Enter password:
nuws_data_db
....
```

- Once you have your MYSQL database set up on your machine you have to run the backend data pipeline service.

- Go to "nuws-api-v1" folder and execute the data pipeline service NB: Remember to store your PASSWORD environment variable

```console
raymond@raymond-ThinkPad-T480:~/nuws-api-v1$ python3 -m etl.main https://kc.kobotoolbox.org/api/v1/data/1330078
....
```

- Once ETL Data process is successfully completed. In the "nuws-api-v1" folder, execute the backend RESTful API service

```console
raymond@raymond-ThinkPad-T480:~/nuws-api-v1$ python3 -m api.v1.app
* Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
...
```

### (2) Simply run the docker container on your local machine

- Include all neccessary steps needed to run docker container for flask RESTful API here.

## Usage :open_file_folder:

0. See Water Schemes managed by NUWS Water Utility
![States](doc/states.png)

1. See Districts served by NUWS Water Utility
![Amenities](doc/amenities.png)

2. See Villages served by NUWS Water Utility
![Articles](doc/articles.png)

## API Documentation Support :email:

Visit:

- [Project Landing Page](https://www.onirele.tech/nuws-api-v1)
- [API Documentation](http://0.0.0.0:5000/)
- API Documentation accessible once web application is running

## Authors and acknowledgment :school:

Raymond Lukwago Abdul Rauf is a Civil and Environmental Engineer. He has spent the last decade of his career building physical infrastructure aimed at improving people's quality of life. With an interest to data engineering, Raymond is now focusing developing data centric software that will improve transperency around performance monitoring of development programmes using tools such as Python, R, Javascript and C.

## Bugs :bug:

Some API endpoint features not yet active. 

## License :warning:
Public Domain. No copy write protection.

## Authors :black_nib:
- Raymond Lukwago - [Github](https://github.com/lukwagoraymond) / [Twitter](https://twitter.com/lukwagoraymond)  

