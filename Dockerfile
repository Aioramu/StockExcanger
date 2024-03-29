FROM python:3.10
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN apt-get update
RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 \
    libnspr4 libnss3 lsb-release xdg-utils libxss1 libdbus-glib-1-2 \
    curl unzip wget \
    xvfb

RUN echo "===> Installing system dependencies.." && \
    apt-get update && apt-get install --no-install-recommends -y python3 python3-pip wget libxtst6 fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 \
    libnspr4 libnss3 lsb-release xdg-utils libxss1 libdbus-glib-1-2 libgbm1 $BUILD_DEPS xvfb curl vim && \
     rm -rf /var/lib/apt/lists/* && \
    \
    echo "===> Installing geckodriver.." && \
    wget https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz && \
    tar -zxf geckodriver-v0.31.0-linux64.tar.gz -C /usr/local/bin && \
    chmod +x /usr/local/bin/geckodriver && \
    rm geckodriver-v0.31.0-linux64.tar.gz &&\
    \
    echo "===> Installing firefox.." && \
    wget "https://download.mozilla.org/?product=firefox-latest&os=linux64" && \
    tar -xjf $(ls | grep firefox*) -C /opt/ && \
    ln -s /opt/firefox/firefox /usr/bin/firefox
    #RUN rm firefox*.tar




# install phantomjs

RUN wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2 && \
    tar -jxf phantomjs-2.1.1-linux-x86_64.tar.bz2 && \
    cp phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/local/bin/phantomjs && \
    rm phantomjs-2.1.1-linux-x86_64.tar.bz2

RUN pip install -r requirements.txt
COPY . /code/
