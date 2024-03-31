### clone

git clone --branch dev https://github.com/linhthi/hannom_anntotation_tool.git

### Data

https://drive.google.com/drive/folders/1AqOqis_9wKTnn4siyx6cuznBUKY2F8Qe?usp=sharing

### Backend

Config at: config.py

Move to frontend directory:

```
cd back_end
```

Install packages:

```
pip3 install -r requirements.txt
```

Run backend:

```
python3 app.py
```

### Frontend

Config at: front_end/tool_annotator/.env
package.json: "proxy": "http://127.0.0.1:5001/",

Move to frontend directory:

```
cd front_end/tool_annotator
```

Install all dependency:

```
npm install
```

Start front_end:

```
set NODE_OPTIONS=--openssl-legacy-provider
npm start
```

### Docker:

```
docker-compose up
```

### Access

http://localhost:3003/images
