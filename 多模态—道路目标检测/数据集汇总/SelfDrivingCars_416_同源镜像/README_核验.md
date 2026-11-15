# Self Driving Cars 同源镜像

- 来源：<https://huggingface.co/datasets/ayoubsa/Sign_Road_Detection_Dataset>
- 原项目：<https://universe.roboflow.com/selfdriving-car-qtywx/self-driving-cars-lfjou/dataset/4>
- 许可：镜像说明为 CC BY 4.0；使用时应同时注明原项目和镜像来源。
- 实测：train 3530 图/3530 YOLO 标签，valid 801 图/801 YOLO 标签，test 638 图/无标签；示例图尺寸 416×416。
- data.yaml 中类别 ID 与类别名取自镜像作者发布的模型权重元数据，未执行模型反序列化。
- 测试集仅可用于预测展示，不能计算测试 mAP。验证集有标签，可用于训练过程评估。
- 论文英文发表版的源数据 v4 是 640×640。需要严格复现实验时，应从 Roboflow v4 导出原版数据，并保留版本号与导出日期。
