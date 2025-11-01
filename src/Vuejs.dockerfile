FROM node:lts-alpine

WORKDIR /application/client

COPY ./application/client .

RUN npm install

RUN npm run build
CMD ["npm", "run", "host"]