# Use the official Node.js image
FROM node:18-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json into the container
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY frontend/ ./

# Build the React application
RUN npm run build

# Install 'serve' globally to serve the static files
RUN npm install -g serve

# Expose the port that the app runs on
EXPOSE 3000

# Start the app
CMD ["serve", "-s", "build", "-l", "3000"]