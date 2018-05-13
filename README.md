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

---

Progress update:

    # deploy
    - docker-compose and basic dockerfiles finished, although containers run on
      root, some people object to that (heroku won't run such containers for
      example)
    - I planned nginx + docker-gen + docker-letsencrypt-nginx-proxy-companion
      but did not start
    - Ansible deploy not started

    # frontend
    - there are bugs in the frontend preventing containerized run
    - reasonably finished, learned quite some basic react, the code is rather
      horrible but not dumb
    - editing of a task not finished, the code was not DRYed
    - no tests

    # backend
    - models and API work, they are very basic, this is a simple app
    - no tests, no login, no security, minimalism


# test containers locally

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
