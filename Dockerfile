FROM python:3.10-alpine

RUN apk add --update bash curl unzip zip rust cargo linux-headers

ARG TERRAFORM_VERSION="1.4.6"
ARG GCLOUD_VERSION="428.0.0"

RUN curl https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip -o terraform_${TERRAFORM_VERSION}.zip && \
  unzip terraform_${TERRAFORM_VERSION}.zip -d /bin && \
  rm -f terraform_${TERRAFORM_VERSION}.zip

RUN curl https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-${GCLOUD_VERSION}-linux-x86_64.tar.gz -o gcloud_${GCLOUD_VERSION}.tar.gz && \
  mkdir -p /usr/local/gcloud && \
  tar -xf gcloud_428.0.0.tar.gz -C /usr/local/gcloud && \
  /usr/local/gcloud/google-cloud-sdk/install.sh --quiet

ENV PATH $PATH:/usr/local/gcloud/google-cloud-sdk/bin

WORKDIR /app
COPY . /app/

RUN pip install poetry && \
  poetry install --without=experiment

