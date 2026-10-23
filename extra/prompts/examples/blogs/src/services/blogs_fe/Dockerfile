FROM node:18-alpine

# install pkg dependencies
RUN apk update && apk add \
    make

# install dev pkg dependencies
RUN apk update && apk add \
    curl \
    fish \
    nano

WORKDIR /app/src