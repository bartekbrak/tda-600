---
# tda-600

The repository will contain a simple todo app for a perspective employer. The
stack includes django, react, postgres and docker. As with code written outside
business context, the app will differ from my usual coding style which is
"minimalism and no gold-plating, test heavily but only end-to-end tests with
unit tests only when required, comment heavily". The context of this app is a
show of my technical skills, therefore, I will follow assignment requirements,
choose careful standard style and probably do an overkill to demonstrate my
abilities.

Since this is developed in my free time, I will take this opportunity to learn
something new and use React, which I have never used before. I will follow parts
of [react tutorial](https://reactjs.org/tutorial/tutorial.html) but also check
against http://todomvc.com/ when confused taking care not to use too much of
their code.

# deploy

The deploy to cloud should be straightforward to those familiar with docker[compose].
I planned to add pre-orchestration with Ansible but time is running out on me.

Note two env variables:
- CORS_ORIGIN_WHITELIST - whom should backend welcome
- REACT_APP_BACKEND_HOST - where is backend located

For the domains front1.com, front2.com, backend.com,
one should provide these values in docker-compose.yml:

    ...
    services:
      frontend:
        build:

        args:
          REACT_APP_BACKEND_HOST: http://backend_CHANGE_THIS.com
    ...
      backend:
        environment:
          CORS_ORIGIN_WHITELIST: http://front1.com,http://front2.com

Two frontends are rather strange, this here is to demonstrate
the relationships and capabilities.

# test containers manually locally

    pip install docker-compose
    docker-compose up -d
    # visit localhost:3000 and localhost:8000

# local development, rough instructions

    sudo apt install python3.6-dev postgres yamllint zlib1g-dev
    # get docker > 18.03 because https://github.com/docker/cli/pull/886
    # if ubuntu
    ./ubuntu_init
    # get node
    # https://nodejs.org/en/download/package-manager/#debian-and-ubuntu-based-linux-distributions
    curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
    # I prever yarn, feel free to use npm
    curl -sL https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
    echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
    sudo apt-get update && sudo apt-get install yarn
    ./plough_and_populate_db.sh 7
    cd backend
    ./manage.py runserver
    cd ../frontend
    yarn install
    yarn start

# run tests

pip install -r backend/requirements_dev.txt
pytest
