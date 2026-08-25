# https://hub.docker.com/_/node
FROM node:alpine as builder
# werkmap binnen de container
WORKDIR /usr/app
# eerst dependencies
COPY ./package.json ./package.json
RUN npm install
# dan de rest van de copies
COPY ./src .
# daar zit ook npm bij (relatief zwaar), die kun je nu gebruiken
# CMD [ "npm", "start" ]
CMD npm run build

# distribute ready making
FROM nginx:alpine

# TODO: path aanpassen
COPY --from=builder /usr/app/dist /usr/share/nginx/html         