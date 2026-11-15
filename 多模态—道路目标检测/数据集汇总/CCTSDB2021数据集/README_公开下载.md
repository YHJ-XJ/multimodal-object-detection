# CCTSDB2021：公开下载与本地归档核验

**这个公开仓库没有托管 CCTSDB2021 的图片、解压目录或任何数据 ZIP，包括 `train_img.zip`。** 本目录中的 `README.md` 和 `README_核验.md` 记录的是本地资料文件夹的保存情况，不能当作 GitHub 的可下载文件清单。

请从作者发布入口获取数据：

- [CCTSDB2021 作者仓库](https://github.com/csust7zhangjm/CCTSDB2021)
- [作者 Google Drive 文件夹](https://drive.google.com/drive/folders/14Km2W-5hbixXDfz7WSqW_Rx7O5m8ZMFn?usp=sharing)
- [作者百度网盘文件夹](https://pan.baidu.com/s/1hyGmwLzcPi21XEP1MQsj5Q)，提取码 `nygx`

作者仓库列出了数据获取入口及引用要求。其 GitHub 仓库带 GPL-3.0 许可文件，但没有明确说明该许可是否覆盖另存在 Google Drive / 百度网盘的完整 ZIP。因此这里仅提供作者下载入口，不把这些外部压缩包复制到本公开仓库。

## 本地归档中的文件

下表是本地已下载文件的**实测**大小和 SHA-256，用于核对同一版本的下载结果；并非作者发布的校验值。若作者更新了文件，以作者发布的新版本为准。

| 文件名 | 字节数 | SHA-256 |
| --- | ---: | --- |
| `train_img.zip` | 1,259,763,275 | `fb9be19f745ee0e9774934512c26db07a4da37540b2f42ed4116a33b667c643d` |
| `test_img.zip` | 294,210,884 | `3e01183148ff240a5e27721919719c8f912ac649ab512a0011941e4778e1a676` |
| `train_labels.zip` | 3,350,861 | `31c56e3316807f01c91e4a6e638963b6fa4bbb623f44e3790da770384c10ad46` |
| `test_labels.zip` | 319,377 | `459ac45e63a8c31986d296208013daf68e340318899562e98987658ae9c265ec` |
| `xml.zip` | 8,143,446 | `35c1f3b7cdfde8e5ddded9c186e16335b2f24364ebd00c2be95bdcfca4051329` |
| `Classification based on size of traffic signs.zip` | 630,398 | `6e2fbb325c89732254e16df33577f1f6b94b382d682a38f65dd06e7eff4bc238` |
| `Classification based on weather and environment.zip` | 925,344 | `18c02af83fac00fa0ab85a0eb7247d27c4043e0b337c9897a3a780c360a6d2dc` |

在 Windows PowerShell 中，可用 `Get-FileHash -Algorithm SHA256 -LiteralPath 'train_img.zip'` 核对下载后的文件。训练图像在 `train_img.zip` 中；作者还提供测试图像、标签和按天气/尺寸分类的标注包。
