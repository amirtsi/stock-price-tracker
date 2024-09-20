# Use the official Node.js image as the base image
FROM node:16 as build

# Set working directory
WORKDIR /usr/src/app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the React app for production
RUN npm run build

# Use a lightweight web server to serve the production build
# Start from a new, clean image (to keep it lightweight)
FROM nginx:alpine

# Copy the built files from the previous step
COPY --from=build /usr/src/app/build /usr/share/nginx/html

# Expose port 80 for the application
EXPOSE 80

# Start the web server
CMD ["nginx", "-g", "daemon off;"]
