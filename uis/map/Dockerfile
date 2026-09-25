FROM node:24

WORKDIR /app

COPY package.json ./
COPY yarn.lock* ./
RUN yarn install --frozen-lockfile || yarn install
COPY . .

# Cloud: bake XYZ host into the image. uis[].env only accepts service
# placeholders like api.api — literal URLs must live here / in .env.
ENV VITE_ENV=PRO
ENV XYZ_URL=spai.staging.xyz.earthpulse.ai
ENV STORAGE_NAME=data
RUN printf "VITE_ENV=PRO\nXYZ_URL=spai.staging.xyz.earthpulse.ai\nSTORAGE_NAME=data\n" > .env

EXPOSE 80

CMD yarn run build && yarn run preview --host 0.0.0.0 --port 80
