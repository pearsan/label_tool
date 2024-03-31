FROM node:14.18.0

WORKDIR /app/front_end/tool_annotator

COPY ./src ./src
COPY ./public ./public
COPY package*.json ./
COPY .env ./

RUN npm install

CMD ["npm", "start"]