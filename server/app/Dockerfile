FROM node:lts

# ENV NODE_ENV=production

WORKDIR /usr/src

RUN npm install -g --unsafe-perm elm 

COPY . .

RUN yarn

CMD [ "yarn", "start" ]

