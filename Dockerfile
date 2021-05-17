FROM ubuntu:18.04

COPY . . 

RUN apt-get update
RUN apt-get install -y python3-pip \
	 build-essential \
	 git

CMD ["make", "all"]
