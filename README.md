


# Studium

You can find the project at [http://www.synapsapp.com/](http://www.synapsapp.com/).

## Contributors

|                                       [Amer Mahyoub](https://github.com/ameralhomdy)                                        |                                       [Ben Whitman](https://github.com/b-whitman)                                        |                                       [Cai Nowicki](https://github.com/dunkelweizen)                                        |
| :-----------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------: |
|                      [<img src="https://avatars0.githubusercontent.com/u/18502421?s=400&u=0968b250d7df526da558e489c8b6a3bcca492a0b&v=4" width = "200" />](https://github.com/ameralhomdy)                       |                      [<img src="https://ca.slack-edge.com/ESZCHB482-W012JQ0JDDZ-c45d031dd395-512" width = "200" />](https://github.com/b-whitman)                       |                      [<img src="https://avatars1.githubusercontent.com/u/53185634?s=400&v=4" width = "200" />](https://github.com/dunkelweizen)                       |                      [<img src="https://www.dalesjewelers.com/wp-content/uploads/2018/10/placeholder-silhouette-female.png" width = "200" />](https://github.com/)                       |                      [<img src="https://www.dalesjewelers.com/wp-content/uploads/2018/10/placeholder-silhouette-male.png" width = "200" />](https://github.com/)                       |
|                 [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/ameralhomdy)                 |            [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/b-whitman)             |           [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/dunkelweizen)             |
| [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com//in/amermahyoub/) | [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/benjamin-whitman-946a0a192/) | [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/cai-nowicki-82749312/) |



[![Maintainability](https://api.codeclimate.com/v1/badges/ec33ec3ad4fd03a44fb0/maintainability)](https://codeclimate.com/github/Lambda-School-Labs/pt-synaps-ds/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/ec33ec3ad4fd03a44fb0/test_coverage)](https://codeclimate.com/github/Lambda-School-Labs/pt-synaps-ds/test_coverage)


## Project Overview


 [Trello Board](https://trello.com/b/TIZq1yva/labspt11-studium)

 [Product Canvas](https://www.notion.so/244664dd54b047b5803cbd5c735dfb31?v=766ef77c015042b3b7fbec64394693e9)

A flashcard application for students studying life sciences. It's Quizlet meets Anki 

Data Science contribution to the project is a Heroku API with endpoints that will return auto-generated text for flashcards, a set of auto-generated cards for a deck on a specific term, dates for the next time to show the user a specific flashcard based on the Leitner spaced repetition system, or metrics/visualizations for the user's studying sessions.

[Deployed Front End](https://studium-fe.herokuapp.com/)

### Tech Stack
- Python
- Wikipedia access through MediaWiki API
- Heroku (both front-end and custom API)
- FastAPI

### Data Sources


-   [MediaWiki API on Wikipedia.org] (https://en.wikipedia.org/w/api.php)
-   [User Data from app] 


### How to connect to the web API

You can connect to the DS web api by sending a GET or POST requests. 
Go to https://studium-ds.herokuapp.com/docs for full documentation. All features of the API can be trialed from the FastAPI docs page.



## Contributing

When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the owners of this repository before making a change.

Please note we have a [code of conduct](./code_of_conduct.md.md). Please follow it in all your interactions with the project.

### Issue/Bug Request

 **If you are having an issue with the existing project code, please submit a bug report under the following guidelines:**
 - Check first to see if your issue has already been reported.
 - Check to see if the issue has recently been fixed by attempting to reproduce the issue using the latest master branch in the repository.
 - Create a live example of the problem.
 - Submit a detailed bug report including your environment & browser, steps to reproduce the issue, actual and expected outcomes,  where you believe the issue is originating from, and any potential solutions you have considered.

### Feature Requests

We would love to hear from you about new features which would improve this app and further the aims of our project. Please provide as much detail and information as possible to show us why you think your new feature should be implemented.

### Pull Requests

If you have developed a patch, bug fix, or new feature that would improve this app, please submit a pull request. It is best to communicate your ideas with the developers first before investing a great deal of time into a pull request to ensure that it will mesh smoothly with the project.

Remember that this project is licensed under the MIT license, and by submitting a pull request, you agree that your work will be, too.

#### Pull Request Guidelines

- Ensure any install or build dependencies are removed before the end of the layer when doing a build.
- Update the README.md with details of changes to the interface, including new plist variables, exposed ports, useful file locations and container parameters.
- Ensure that your code conforms to our existing code conventions and test coverage.
- Include the relevant issue number, if applicable.
- You may merge the Pull Request in once you have the sign-off of two other developers, or if you do not have permission to do that, you may request the second reviewer to merge it for you.

### Attribution

These contribution guidelines have been adapted from [this good-Contributing.md-template](https://gist.github.com/PurpleBooth/b24679402957c63ec426).

## Documentation

See [Backend Documentation](https://github.com/Lambda-School-Labs/Studium-be) for details on the backend of our project.

See [Front End Documentation](https://github.com/Lambda-School-Labs/Studium-fe) for details on the front end of our project.
