# syntax=docker/dockerfile:1
FROM node:20-alpine AS build

WORKDIR /app

COPY package.json ./
RUN npm install

COPY tsconfig.json tsconfig.node.json vite.config.ts index.html ./
COPY src ./src

ARG VITE_API_BASE_URL
ARG VITE_API_PREFIX=/api/v1
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}
ENV VITE_API_PREFIX=${VITE_API_PREFIX}

RUN npm run build

FROM nginx:1.25-alpine

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
