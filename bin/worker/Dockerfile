FROM python:3.8-buster

ENV PATH=$PATH:/root/.axiom/interact
ENV HOME="/root/"

RUN apt-get update \
    && apt-get install -yq apt-utils build-essential curl gcc wget \
    readline-common neovim git zsh zsh-syntax-highlighting zsh-autosuggestions jq build-essential python3-pip unzip git p7zip libpcap-dev rubygems ruby-dev grc

WORKDIR /root/.axiom
RUN git clone https://github.com/pry0cc/axiom /root/.axiom/
RUN  wget -q -O /tmp/doctl.tar.gz https://github.com/digitalocean/doctl/releases/download/v1.66.0/doctl-1.66.0-linux-amd64.tar.gz && tar -xvzf /tmp/doctl.tar.gz && mv doctl /usr/bin/doctl && rm /tmp/doctl.tar.gz
RUN interact/axiom-configure --config "{}" --unattended
RUN /usr/local/go/bin/go install -v github.com/projectdiscovery/notify/cmd/notify@latest

RUN git clone https://github.com/pry0cc/proteus /app && cd /app 
RUN pip3 install -r /app/bin/worker/requirements.txt

ENTRYPOINT ["python3", "/app/bin/worker/worker.py"] 
