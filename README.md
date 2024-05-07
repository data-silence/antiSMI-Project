# antiSMI Project


## Table of contents
* [About project](#about-project)
* [Stats](#stats)
* [Structure](#structure)
* [Stack](#stack)
* [Pipeline](#pipeline)
* [Development Tools](#development-tools)
* [Plans](#plans)
* [Contact info](#contact-info)

![](https://github.com/data-silence/antiSMI-Project/blob/main/img/project.png?raw=true)

## About project

The AntiSMI project explores and creates new ways of working with history through news for readers, journalists and researchers.

It's a personal analytical non-profit project at the intersection of ML and journalism, which allows using machine learning models to analyze changes in the news flow in real time, trying to create a fundamentally different way of consuming news in the conditions of changing the way of its production and in the conditions of misinformation.

The project is currently based on Russian-language news, but has plans to cover news in all key world languages.  


You can use the applications and opportunities of this project right now:
- [Web-app](http://38.242.140.206:8501/) (various tools to research the news flow)
- [Nowdays Bot](https://t.me/antiSMI_bot) (tools for working with current news)
- [Timemachine Bot](https://t.me/time_mashine_bot) (tools for working with past news, temporarily out of service)


## Stats

* **Project start:** 2022-07-01
* **Capacity:** 40 news agencies, ~ 1,000 news/day
* **News categories:** 7
* **Present database capacity:** ~ 400,000 news articles [01.2022 - today]
* **Archive base capacity:** ~ 1,650,000 articles [08.1999 - 01.2022]



## Structure

The project consists of independent parts that deal with news from the past and/or present time.

From a technical point of view, these parts can be grouped into 5 different groups, that are in different repositories and/or on different servers:

1.  **_Scrappers_** [[Collector](https://github.com/data-silence/antiSMI-Collector) and [Parsers](https://github.com/data-silence/Media-Datasets-Parsers)] - collects and processes agency news on a regular basis for use in the rest of the project 
2. **_Databases_** - relational and vector databases that store news collected and processed by Scrappers  
3. [**_Backend_**](https://github.com/data-silence/antiSMI-backend) - FastAPI backend - retrieves various views of news articles stored in the project databases. The backend gets these views to the frontend of applications developed within the project. 
4. **_Frontend_** [[Web-app](https://github.com/data-silence/antiSMI-app), [Nowdays Bot](https://github.com/data-silence/antiSMI-Bot) and [Timemachine Bot](https://github.com/data-silence/timemachine)] - these are different user interfaces for interacting with the project. Web-app - is the most versatile and comprehensive way, bots serve as a mobile way to interact with the current and past news stream. 
5. **_Observer_** - researches social trends, make dashboards and creates NLP models. It is an ApacheSuperset based analytics system that connects to Databases and builds analytical dashboards and reports.

You can access the repositories you are interested in for more details by following the links above. Databases and Observer  are closed parts of the project. This means that you will not be able to reproduce these project data using the source repositories, and docker / docker-compose files, but you will be able to learn and easily understand how to build a similar service yourself.   



## Stack

* **Language:** python, sql 
* **Databases:** postgreSQL + , sqlalchemy
* **Validation:** pydantic
* **Logging:** loguru
* **BI**: apache SuperSet


## Self deploy

It is possible to compose the main parts of the project (Database, Backend and Web-app) using the `docker-compose.yml` file, which is located in the root of this repository
(you must have access to the files in steps 2-3).

1. Clone the 2 repositories on your server side by side into the root of build directory using `git clone https://github.com/data-silence/antiSMI-backend` and `git clone https://github.com/data-silence/antiSMI-app`
2. Create a `db` directory and copy `docker-compose.yml` into the root of build directory   
3. Copy the file with the required environment variables for each part of the project `.env-non-dev` into the root of this part directory. Create directory `models` and copy the categorisation model file `cat_model.ftz` into it
4. Make sure that docker is installed on the server. 
5. Start building the project using `docker up -d`
6. Your database starts on port 5432, your API on port 8000, and your web application on 8501


## Pipeline

- **Scraping**
    - requests
    - beatufill soup 4
- **Summarization**
    - mBart, Seq2Seq, pre-trained [news summary]
    - ruT5, pre-trained [headline]
- **Categorization**
    - fasttext, supervised pre-training, 7 classes (categories)
- **Clustering**
    - Navec glove-embeddings (trained on news corpus)
    - sklearn: agglomerative clustering by cosine distance with tuned thresholding
- **Interaction Interface**
    - pyTelegramBot [user interface]
    - SuperSet [analytics, dashboards]

## Development Tools

- Pycharm
- Docker
- GitHub
- Linux shell


## Plans
- **Common purpose**
    - start public operation of the project 
    - replicate the project for coverage on the news agenda in other countries
- **Collector**
    - increase source coverage: add parsing of English-language, Ukrainian and pro-state news agencies 
- **Bot**
    - audio digests
    - training a neural network model for generating news photos
- **Observer**
    - deploy a remote Superset server
    - increase dashboard coverage of news streams and agency structure
    - write and publish an article based on the results of research and dashboards

## Contact info
* enjoy-ds@pm.me
