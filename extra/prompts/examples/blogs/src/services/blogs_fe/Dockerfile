FROM node:18-alpine

# install pkg dependencies
RUN apk update && apk add \
    bash \
    make \
    py3-pip \
    python3

# Copy each library
COPY libs/jazzoo /app/libs/jazzoo

# Install the libraries
RUN pip install --break-system-packages -e /app/libs/jazzoo

# install dev pkg dependencies
RUN apk update && apk add \
    curl \
    fish \
    nano

WORKDIR /app/src