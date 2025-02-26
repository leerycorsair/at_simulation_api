FROM python:3.12

RUN apt-get update && \
    apt-get install -y wget curl && \
    wget https://go.dev/dl/go1.23.4.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go1.23.4.linux-amd64.tar.gz && \
    rm go1.23.4.linux-amd64.tar.gz && \
    ln -s /usr/local/go/bin/go /usr/bin/go

RUN curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh | sh -s -- -b /usr/local/bin latest && \
    golangci-lint --version

RUN /usr/local/go/bin/go install golang.org/x/tools/cmd/goimports@latest

RUN pip install poetry && \
    poetry config virtualenvs.create false

ENV PATH=$PATH:/root/go/bin

COPY pyproject.toml poetry.lock / 
RUN poetry install --no-root

COPY . .

RUN chmod +x ./application.py

CMD ["poetry", "run", "python", "./application.py"]
