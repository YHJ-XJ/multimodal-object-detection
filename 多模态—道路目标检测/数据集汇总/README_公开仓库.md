# 公开仓库中的数据包

本目录保留了本地资料文件夹的分类方式。各原有核验记录描述的是**本地完整资料**；公开仓库只包含下表列出的可再发布 ZIP 与说明文件，未附解压后的重复副本。

| 数据集 | 仓库状态 | 许可与原始来源 |
| --- | --- | --- |
| Brazil_YOLO11_2026 | 含发布版 ZIP（约 271 MB） | [Zenodo 记录](https://doi.org/10.5281/zenodo.17900512)，CC BY 4.0 |
| SelfDrivingCars_416_同源镜像 | 含 train/valid/test ZIP（镜像版，416×416） | [原 Roboflow 项目](https://universe.roboflow.com/selfdriving-car-qtywx/self-driving-cars-lfjou)，CC BY 4.0；[镜像来源](https://huggingface.co/datasets/ayoubsa/Sign_Road_Detection_Dataset) |
| GTSDB数据集 | 含第三方整理版 train/valid/test ZIP（545 图） | [Roboflow 整理版](https://universe.roboflow.com/mohamed-traore-2ekkp/gtsdb---german-traffic-sign-detection-benchmark/dataset/1)，CC BY 4.0；[Hugging Face 镜像](https://huggingface.co/datasets/keremberke/german-traffic-sign-detection) |
| CCTSDB2021数据集 | 仅来源与核验记录 | [作者仓库](https://github.com/csust7zhangjm/CCTSDB2021)；公开版未附数据包，请按作者页面获取 |
| TT100K数据集 | 仅来源说明 | [清华大学官方页面](https://cg.cs.tsinghua.edu.cn/traffic-sign/)；本地也未下载完整数据 |

ZIP 文件使用 Git LFS。若克隆后看到的是短文本指针，请运行 `git lfs pull`。解压后按各目录的 README 核对划分、类别和图像尺寸。Brazil 的 `data_local.yaml` 是本地路径配置示例；实际训练时按解压位置调整路径。

转载的 CC BY 4.0 数据应保留原作者署名、来源链接与许可，并说明在本仓库中仅重新打包存放或作为镜像收录。不同镜像可能与原版的分辨率、标注或划分不同，不能直接混用实验指标。
