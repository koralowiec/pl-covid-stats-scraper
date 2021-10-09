FROM python:3.9-bullseye

RUN apt-get update && \
  apt-get install -y firefox-esr

RUN cd /tmp && \
  wget https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz && \
  tar -xvzf geckodriver* && \
  chmod +x geckodriver && \
  cp geckodriver /opt

RUN mkdir /scraper && \
  useradd --create-home --shell /bin/bash scraper && \
  chown -R scraper:scraper /scraper

USER scraper

ENV PATH="/opt:${PATH}"

WORKDIR /scraper

COPY --chown=scraper:scraper requirements.txt ./

RUN pip install -r requirements.txt

COPY --chown=scraper:scraper . ./

CMD ["python", "main.py"]
