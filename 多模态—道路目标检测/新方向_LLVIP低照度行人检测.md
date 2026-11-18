# 新方向 LLVIP 低照度行人检测

## 结论

新主线改为 RGB 与热红外配对的低照度行人检测。数据集采用 LLVIP，检测类别只有 `person`。它适合先检验双模态读取、配对和融合是否带来收益，再考虑更难的多类别任务。LLVIP 官方说明现行版本有 15,488 对严格时空对齐的图像，原作者提供了行人标注和 YOLOv5 检测基线。场景以低照度为主，不把它描述成专门的交通数据集。

这次换题目是为了降低入门复杂度，**不保证新数据集的 mAP 一定更高**。单类 LLVIP 与六类 M3FD 的 mAP 不可直接比较，必须先在同一 LLVIP 测试集上比较 RGB、热红外、RGB＋热红外三组。

可作为量级参考的是 [MCFusion 论文](https://www.mdpi.com/1999-4893/19/6/468)：其 LLVIP 上 YOLOv11n RGB 对照组报告 `mAP50=87.8%`、`mAP50-95=49.4%`；特定双分支直接融合组报告 `mAP50=94.7%`、`mAP50-95=59.1%`。这是论文自己的模型和协议结果，本项目四通道早期融合不能直接照搬这些数值。

## 数据与许可

- 作者项目：https://github.com/bupt-ai-cz/LLVIP
- 作者下载清单：https://github.com/bupt-ai-cz/LLVIP/blob/main/download_dataset.md
- 作者论文：https://openaccess.thecvf.com/content/ICCV2021W/RLQ/papers/Jia_LLVIP_A_Visible-Infrared_Paired_Dataset_for_Low-Light_Vision_ICCVW_2021_paper.pdf
- 许可：https://github.com/bupt-ai-cz/LLVIP/blob/main/Term%20of%20Use%20and%20License.md
- 作者 Google Drive：https://drive.google.com/file/d/1VTlT3Y7e1h-Zsne4zahjx5q0TK2ClMVv/view
- 作者百度网盘：https://pan.baidu.com/s/1eQO1Is2NPyd-mgmv1Csbfg ，提取码 `14lc`

作者 Google Drive 下载目前触发限流。本地另从公开镜像 `McCheng/LLVIP` 获取压缩包用于**本机非商业研究**；镜像地址为 https://huggingface.co/datasets/McCheng/LLVIP 。它不是作者官方发布入口，因此必须核对压缩包完整性、图片和标签数量、配对 ID、标注结构，并记录 SHA256。不要将图像或原始标注上传到公开 GitHub 仓库；公开仓库只保留脚本、来源和下载索引。

## 数据划分和基线

保留原作者 `train` 与 `test` 两组。只从原训练集划出验证集，按文件名前两位的组整体划分，避免同一组相邻图像同时进入训练与验证。两位前缀是否确实对应采集场景没有官方元数据证明，因此方案称为“文件名前缀分组”，不写成官方场景划分。实际划分是训练 10,436、验证 1,589、作者测试 3,463 对；验证集占作者训练集的 13.2%。保存 `split_manifest.csv`，三组实验复用同一份划分。

| 组别 | 输入 | 模型 | 用途 |
| --- | --- | --- | --- |
| A | RGB | YOLO11n | 单模态对照 |
| B | 热红外 | YOLO11n | 单模态对照 |
| C | RGB 3 通道＋热红外 1 通道 | YOLO11n | 早期融合入门基线 |

全量 15,488 对已完成转换与核验，原始 XML 中 5 个零宽度框已跳过，其余保留 42,432 个有效框。30 对小样本的 1 轮 CPU 训练验证了四通道输入和测试流程；正式准确率尚未产生。8GB 显存初跑 `imgsz=640`、`batch=4`、`epochs=100`；所有组统一设置。准确率报告 `mAP50-95`、`mAP50`、召回率、误检数、夜间失败案例和速度。融合模型仍应与两种单模态在**同一个官方测试集**上比较；若 C 不优于 B，不要仅凭单类 AP 高就宣称融合有效。

## 运行

本机数据已完成转换，直接核验：

```powershell
py -3.14 .\基线代码\verify_llvip_prepared.py --root 'D:\rgbt_data\LLVIP_prepared'
```

重新生成时请给 `prepare_llvip.py` 指定新的空目录；现有 `D:\rgbt_data\LLVIP_prepared` 不应当作新输出目录覆盖。

转换结果的 `rgb`、`thermal`、`rgbt` 目录分别含 `data.yaml`。训练环境按 [基线代码说明](基线代码/README.md) 安装后运行：

```powershell
& $trainPy .\基线代码\train_llvip.py --mode rgb --epochs 100
& $trainPy .\基线代码\train_llvip.py --mode thermal --epochs 100
& $trainPy .\基线代码\train_llvip.py --mode rgbt --epochs 100
```

M3FD 既有原始包、脚本与方案保留，供后续多类别研究和结果核对。当前项目目录尚未找到 M3FD 的 `results.csv`、`baseline_result.json` 或权重，无法据此判断旧基线低分究竟来自数据难度、训练设置还是标注问题。
