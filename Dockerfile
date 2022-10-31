# starting with latest python image
FROM python:latest

# making a directory for the webscraper
RUN mkdir /whiskywebscraper
# adding trusted keys
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# downloading google chrome
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
# updating apt-get
RUN apt-get -y update
# installing google chrome
RUN apt-get install -y google-chrome-stable
# downloading selenium chromedriver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
# unzipping the selenium zip file
RUN apt-get install -yqq unzip
# installing selenium chromedriver
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# the working directory
WORKDIR /whiskywebscraper

# add entire contents of this folder to the image
COPY . .

# install library requirements
RUN pip install -r requirements.txt

# execute main.py
ENTRYPOINT ["python3", "main.py"]