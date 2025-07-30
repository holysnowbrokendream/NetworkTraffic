# 构建阶段 - 使用官方Node.js镜像
FROM node:18 as build-stage

WORKDIR /app

# 复制package文件
COPY package*.json ./

# 强制更新package.json中的版本
RUN sed -i 's/"vite": "^7.0.1"/"vite": "^5.0.0"/g' package.json && \
    sed -i 's/"@vitejs\/plugin-vue": "^6.0.0"/"@vitejs\/plugin-vue": "^5.0.0"/g' package.json

# 清理并重新安装依赖
RUN rm -rf node_modules package-lock.json && \
    npm install

# 复制源代码
COPY . .

# 设置NODE_ENV为production
ENV NODE_ENV=production

# 构建Vite应用
RUN npm run build

# 生产阶段 - 使用nginx服务静态文件
FROM nginx:alpine as production-stage

# 复制构建产物（Vite默认输出到dist目录）
COPY --from=build-stage /app/dist /usr/share/nginx/html

# 复制nginx配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露端口
EXPOSE 80

# 启动nginx
CMD ["nginx", "-g", "daemon off;"] 