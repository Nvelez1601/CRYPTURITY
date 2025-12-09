# syntax=docker/dockerfile:1
FROM node:20-alpine AS build

ARG FRONTEND_PATH=.

WORKDIR /app

# Copy dependency manifest and install in a clean layer so caches survive
COPY ${FRONTEND_PATH}/package.json ./
RUN npm install

# Bring over the rest of the build inputs from the configured source tree
COPY ${FRONTEND_PATH}/tsconfig.json ${FRONTEND_PATH}/tsconfig.node.json ${FRONTEND_PATH}/vite.config.ts ${FRONTEND_PATH}/index.html ./
COPY ${FRONTEND_PATH}/src ./src

ARG VITE_API_BASE_URL
ARG VITE_API_PREFIX=/api/v1
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}
ENV VITE_API_PREFIX=${VITE_API_PREFIX}

RUN npm run build

FROM nginx:1.25-alpine

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
