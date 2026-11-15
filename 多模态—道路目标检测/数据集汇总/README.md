# 道路标识检测数据集索引

> 公开仓库说明：本页描述本地完整资料的收集和核验状态。GitHub 公开版只上传许可明确的数据 ZIP 与资料索引；实际收录情况见 [README_公开仓库.md](./README_公开仓库.md)。

本目录对应《基于改进 YOLOv11n 的道路标识检测算法研究》。论文实际任务是单目可见光道路标识检测；交通灯和限速牌也计入论文的 15 类。

| 数据集 | 用途 | 本地内容 | 关键差异 |
| --- | --- | --- | --- |
| SelfDrivingCars_416_同源镜像 | 复现论文 15 类任务的起点 | 3530 训练图及标注、801 验证图及标注、638 测试图 | 镜像为 416×416，测试图无标注；论文使用 640×640 |
| CCTSDB2021数据集 | 中国道路场景、复杂天气及目标尺度的外部验证 | 作者发布的图像和标注压缩包 | 仅 3 个大类，不能与 15 类直接合并训练或直接比较 mAP |
| GTSDB数据集 | 德国道路标识小型检测基准 | 545 张标注图，COCO 格式 | 是基于 GTSDB 的第三方整理版，不是官方 900 张原包 |
| Brazil_YOLO11_2026 | 巴西道路标识小范围迁移实验 | 已下载并解压；1959/187/119 张训练/验证/测试图与同数标注 | 6 种巴西交通牌，来源含 Roboflow 数据与数据增强；不可与论文 15 类指标直接比较 |
| TT100K数据集 | 后续小目标扩展实验 | 下载来源说明 | 官方压缩包约 19.2 GB，本轮未纳入本地数据 |

## 论文同源数据集的版本核对

中文稿第 3 节称数据取自 Kaggle，但同一研究的英文发表版在 Data Availability Statement 中明确给出 Roboflow Universe 项目。该项目 v4 为 4969 张、640×640，划分为 3530/801/638；这与中文稿一致。发布页：
https://universe.roboflow.com/selfdriving-car-qtywx/self-driving-cars-lfjou/dataset/4

可直接获取的镜像来自：
https://huggingface.co/datasets/ayoubsa/Sign_Road_Detection_Dataset

镜像的划分和 15 类一致，但图像实测为 416×416，且没有测试集标注。它不能用于严格复现论文的 640×640 数据处理，也不能在没有测试标签时计算测试集 mAP。训练可使用镜像目录中的 data.yaml，并在论文中记录所用版本。

## 外部基准来源

- CCTSDB2021 作者仓库：https://github.com/csust7zhangjm/CCTSDB2021
- GTSDB 官方档案：https://sid.erda.dk/public/archives/ff17dc924eba88d5d01a807357d6614c/published-archive.html
- GTSDB 本地镜像来源：https://huggingface.co/datasets/keremberke/german-traffic-sign-detection
- TT100K 官方来源：https://cg.cs.tsinghua.edu.cn/traffic-sign/
- Brazil YOLO11 数据集：https://doi.org/10.5281/zenodo.17900512 （2026 年发布，CC BY 4.0；发布包 271 MB）

## 候选但尚未下载的外部验证集

- GLARE：https://github.com/NicholasCG/GLARE_Dataset ，逆光标识检测。作者通过 Google Drive 文件夹分享；当前网络无法可靠列出文件，未将其标记为已下载。
- CURE-TSD：https://github.com/olivesgatech/CURE-TSD ，雨、雪、雾等挑战条件视频。作者要求先填写使用申请表，未下载数据。
- CeyRo：https://github.com/oshadajay/CeyRo ，同时含道路标识和交通灯，训练集约 3.64 GB、测试集约 1.1 GB。作者的 Google Drive 样例文件当前提示下载额度限制，未下载数据。
- Street Sign Set：https://huggingface.co/datasets/AlessandroFerrante/StreetSignSet ，63 类、约 7300 张、YOLO 标注；可作为后续类别扩展候选，未下载。

各数据集按原始划分保存。跨数据集实验前需先统一类别定义、标注格式与评测协议。
