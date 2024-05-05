FROM node:20

WORKDIR /app

COPY . /app/

COPY package*.json /app

RUN npm install 

EXPOSE 3000

ENTRYPOINT npm run dev