# Build stage
   FROM node:18-alpine as build

   WORKDIR /app

   # Copy package files and install dependencies
   COPY package*.json ./
   RUN npm install

   # Copy the rest of the application and build
   COPY . ./
   RUN npm run build

   # Production stage
   FROM nginx:alpine

   # Copy the build output from the build stage
   COPY --from=build /app/build /usr/share/nginx/html

   # Copy custom nginx config
   COPY ./nginx.conf /etc/nginx/conf.d/default.conf

   EXPOSE 80

   CMD ["nginx", "-g", "daemon off;"]
