# ---------- Build Stage ----------
FROM node:22-alpine AS builder

WORKDIR /app

COPY package*.json ./

# Faster npm install
RUN npm ci --prefer-offline --no-audit

COPY . .

RUN npm run build

# ---------- Production ----------
FROM nginx:alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
CMD wget -qO- http://127.0.0.1 >/dev/null || exit 1

CMD ["nginx","-g","daemon off;"]