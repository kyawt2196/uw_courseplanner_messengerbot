UW Course Finder/Manager developed during Dubhacks 2016 (Placed Top 6 Teams) :D








To deploy to Heroku

//install and login if you haven't
wget -O- https://toolbelt.heroku.com/install-ubuntu.sh | sh
heroku login
heroku git:remote -a coursefinderbot


//deploy
git push heroku master
