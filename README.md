# antiSMI Project

![](https://github.com/maxlethal/antiSMI-Bot/blob/master/img/bot_presentation.png?raw=true)

## Table of contents
* [Stats](#stats)
* [About project](#about-project)
* [Stack](#stack)
* [Pipeline](#pipeline)
* [Contact info](#contact-info)

## Stats

***Purpose:** analytical news project based on machine learning
* **Start:** 2022-07-01 [project suspended for 2 months in 2022]
* **GitHub code:** [Collector](https://github.com/maxlethal/antiSMI-Collector), [Bot](https://github.com/maxlethal/antiSMI-Bot)  
* **Capacity:** 40 news agencies, 500 news/day
* **Bot database capacity:** > 100,000 news articles
* **Disposable base capacity:** 1.5 million articles [08.1999 - 04.2019]

## About project

AntiSMI project is a personal analytical non-profit project at the intersection of ML and journalism, which allows using machine learning models to analyze changes in the news flow in real time, trying to create a fundamentally different way of consuming news in the conditions of changing the way of its production and in the conditions of misinformation.

The project began with collecting and analyzing information about the partners of the Yandex-news service as of early summer 2022. 

As a prototype for the realization of these ideas, a telegram bot with its analytical system was created and is being improved, which can be used as a personal news aggregator, a system for monitoring the information picture of the day, as well as a research tool for working with news archives.

![AntiSMI structure](https://github.com/maxlethal/antiSMI-Collector/blob/master/img/AntiSMI%20structure%20small.png?raw=true)

The project consists of three parts now:
*  [Collector](https://github.com/maxlethal/antiSMI-Collector) - collects and processes fresh agency news on a regular basis for use in the rest of the project 
*  [Bot](https://github.com/maxlethal/antiSMI-Bot) - creates and sends personal smart news digest via telegram interface 
* **Monitor** - researches social trends, make dashboards and creates NLP models

## Stack

* **Language:** python, sql 
* **Databases:** postgreSQL, sqlalchemy
* **Validation:** pydantic
* **Logging:** loguru
* **BI**: apache SuperSet


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

## Contact info
* maxlethal@protonmail.com
* i@max-science.pro
