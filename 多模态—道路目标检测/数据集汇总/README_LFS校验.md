# 仓库内 ZIP 下载与校验

下列 7 个 ZIP **实际托管在本仓库的 Git LFS**。网页中的小型指针文件不是数据包本体；克隆仓库后运行 `git lfs pull`，或在 GitHub 文件页使用下载操作获取完整文件。

| 数据包 | 字节数 | SHA-256 |
| --- | ---: | --- |
| [Brazil YOLO11 发布包](./Brazil_YOLO11_2026/lunarsigndetect.v15-novo-corrigido.yolov11.zip) | 270,964,294 | `0341380081427670ea26f97c2d567ed51747075fff8a569b04b163f86badcabb` |
| [GTSDB test.zip](./GTSDB数据集/test.zip) | 7,225,691 | `1c6d6263f467797a4d6d5f25ba5521c5351538c984183e4dc0579ad76c75b5e9` |
| [GTSDB train.zip](./GTSDB数据集/train.zip) | 50,502,415 | `3f1ee889a0570f60be10a1f8a493e321ee02a6f087fc1cd92a6578d0bafc0700` |
| [GTSDB valid.zip](./GTSDB数据集/valid.zip) | 14,065,269 | `1db6d2090da430dabc3a67dc98f6437e161488696252b1aaa2c39121a23f12db` |
| [SelfDrivingCars test.zip](./SelfDrivingCars_416_同源镜像/test.zip) | 13,371,570 | `9295208cae937cc9261169371229d305ea7f44e278f8aec7ff5d220ff0c94e60` |
| [SelfDrivingCars train.zip](./SelfDrivingCars_416_同源镜像/train.zip) | 71,789,532 | `5654556eddf2788df5603041bc4c866a350916e4bdc1128506689182c4e60a3d` |
| [SelfDrivingCars valid.zip](./SelfDrivingCars_416_同源镜像/valid.zip) | 16,346,163 | `41f87b32682fe19e8bfb5021bfbe959462ab5589df2368eecf36e8b187e0c5ff` |

这些值在上传前由本地原始 ZIP 计算。2026-11-15 从远端 LFS 重新下载了 `GTSDB/test.zip` 与 `SelfDrivingCars/test.zip`，下载后的字节数和 SHA-256 与上表一致。其余 5 个文件已由 Git LFS 上传完成，尚未逐个重新下载核对。

Windows PowerShell 示例：`Get-FileHash -Algorithm SHA256 -LiteralPath 'train.zip'`。如果文件只有约 130 字节，表示当前拿到的是 LFS 指针，需执行 `git lfs pull`。
