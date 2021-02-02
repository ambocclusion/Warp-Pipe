FROM python:latest

WORKDIR /usr/src/app

ENV DISCORDTOKEN ABCDEFGHIJKL
ENV SLACKTOKEN xoxb-ABCDEFGHIJKL
ENV DISCORDCHANNEL 1234567890
ENV SLACKCHANNEL C0123456789

VOLUME /state

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./warppipe.py" ]