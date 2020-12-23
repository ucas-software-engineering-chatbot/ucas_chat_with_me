1. 运行指导：
   - 拷贝文件mse-15-0.1046.h5到flaskr中
   - 拷贝facebank.pkl到flaskr/data中，拷贝haarcascade_frontalface_alt.xml到flaskr/data中，拷贝mmod_human_face_detector.dat到flaskr/data中。
   - 拷贝starImages文件夹到flaskr中。
   - 拷贝model_final.pth到flaskr/starface/arcface/weight/model_final.pth
2. 打开命令行，cd到facial-beauty-prediction中，并执行以下代码
    ```
    export FLASK_APP=flaskr
    export FLASK_RUN_PORT=3000
    flask run            
    ```
    即可运行此代码