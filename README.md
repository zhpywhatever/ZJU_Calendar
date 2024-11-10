# ZJU_Calendar

## 启动前端
cd dayspan-frontend
npm install
npm run serve

## 启动后端
cd LLM_Backend/server
python main.py

## 启动爬虫
cd LLM_Backend/spider1
python main.py

## 将爬取到的本地json经coze_bot精简后插入数据库notices.db
cd LLM_Backend/spider1
python test.py
