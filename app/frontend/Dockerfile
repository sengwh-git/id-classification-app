# frontend/Dockerfile

FROM node:20.18.0-alpine

WORKDIR /app/

# copy code
COPY package*.json /app/
COPY public/ /app/public
COPY src/ /app/src

RUN npm install

EXPOSE 3000

CMD ["npm", "start"]