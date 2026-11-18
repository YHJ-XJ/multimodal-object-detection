# LLVIP 双模态行人检测基线

此目录新增 `prepare_llvip.py` 和 `train_llvip.py`。原始数据来源、许可、镜像核验状态见 [`数据来源与核验.md`](../数据集汇总/LLVIP_低照度行人检测/数据来源与核验.md)。完整压缩包已下载并校验；模型训练指标尚未产生。

## 准备数据

首次准备数据时，从项目根目录执行，先用一个新的空目录检查配对、XML 转 YOLO 和四通道 TIFF：

```powershell
py -3.14 .\基线代码\prepare_llvip.py --limit 20 --out 'D:\rgbt_data\LLVIP_smoke'
```

完整转换前确认 D 盘空余空间；原始包约 4 GB，生成 RGB、热红外及四通道 TIFF 后占用会明显增加。用一个**新的空目录**保存正式版本。本机的 `D:\rgbt_data\LLVIP_prepared` 已有完整结果，复现时应改用新的路径：

```powershell
py -3.14 .\基线代码\prepare_llvip.py --out 'D:\rgbt_data\LLVIP_prepared_new'
py -3.14 .\基线代码\verify_llvip_prepared.py --root 'D:\rgbt_data\LLVIP_prepared_new'
```

准备脚本保留作者 `test`，从作者 `train` 按文件名前两位分组划出验证集，并写入 `split_manifest.csv`。三种模式都使用同一组样本与目标框。`--limit 20` 是格式测试，不能拿它的检测指标当成完整数据基线。Windows 的 OpenCV 读取四页 TIFF 时要求输出目录采用纯英文路径；本机数据集目录下的 `基线准备_可训练` 是指向 `D:\rgbt_data\LLVIP_prepared` 的联接，实际训练与 YAML 都使用 D 盘英文路径。

本机全量数据已经准备并通过核验：训练 10,436、验证 1,589、测试 3,463 对；三组 ID 与标签相同。验证集是作者训练集的 13.2%，比设定的 15% 略少，因为下一整个前缀组会造成过大超额。`split_manifest.csv` SHA256 见数据来源与核验文档。

全量 XML 审计发现 5 个零宽度框，转换时会跳过并在 `preparation_summary.json` 记录。若转换因断电或异常中断，使用相同压缩包、种子和参数加 `--resume` 重跑；已有文件会被覆盖，完成后执行核验脚本。核验脚本检查三组文件 ID、标签、划分隔离和抽样 TIFF 四通道一致性。

## 训练

本机 `D:\rgbt_env` 已安装 PyTorch 2.15.0 CPU 版及 Ultralytics 8.4.215，可做小样本管线检查。正式 GPU 训练前需按 [PyTorch 官方安装页](https://pytorch.org/get-started/locally/)在此环境安装匹配的 CUDA 版 PyTorch，并确认下面的 `torch.cuda.is_available()` 返回 `True`。当前官方 CUDA 轮子下载较慢，因此下列 100 轮训练尚未执行。

```powershell
$trainPy = 'D:\rgbt_env\Scripts\python.exe'
$dataRoot = 'D:\rgbt_data\LLVIP_prepared'
& $trainPy -c "import torch, ultralytics; print(torch.__version__, ultralytics.__version__, torch.cuda.is_available())"
& $trainPy .\基线代码\train_llvip.py --mode rgb --data-root $dataRoot --epochs 100
& $trainPy .\基线代码\train_llvip.py --mode thermal --data-root $dataRoot --epochs 100
& $trainPy .\基线代码\train_llvip.py --mode rgbt --data-root $dataRoot --epochs 100
```

先用 `--epochs 1` 检查每组读入、标签可视化与四通道输入；正式三组使用相同参数。训练脚本在作者 `test` 集评测，保存 `baseline_result.json`。YOLO11n 四通道实验使用真实配对热红外，不以灰度 RGB 伪造红外。

CPU 环境只用于 30 对样本的格式试跑；此结果不能当作研究基线：

```powershell
& $trainPy .\基线代码\train_llvip.py --mode rgbt --data-root 'D:\rgbt_data\LLVIP_thread_smoke' --run-root 'D:\rgbt_runs\LLVIP_smoke' --epochs 1 --batch 2 --device cpu
```

若完整数据转换后的 `rgbt` 目录过大，可以先只生成 `rgb` 与 `thermal`：

```powershell
py -3.14 .\基线代码\prepare_llvip.py --modes rgb thermal --out 'D:\rgbt_data\LLVIP_single_modal'
```

后续四通道版本应使用相同 `seed` 和数据源，并核对 `split_manifest.csv`，确保划分完全一致。
