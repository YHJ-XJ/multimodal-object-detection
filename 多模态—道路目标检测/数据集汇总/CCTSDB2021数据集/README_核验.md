# CCTSDB2021 作者原版

- 作者仓库：<https://github.com/csust7zhangjm/CCTSDB2021>
- 作者 Google Drive：<https://drive.google.com/drive/folders/14Km2W-5hbixXDfz7WSqW_Rx7O5m8ZMFn>
- 数据论文：Zhang 等，CCTSDB 2021: A More Comprehensive Traffic Sign Detection Benchmark，HCIS 2022，DOI 10.22967/HCIS.2022.12.023。
- 原始划分：训练图 16356 张、正样本测试图 1500 张。已保存作者的图像包、YOLO TXT 标注包、完整 XML 包及按天气和目标尺寸分类的 XML 包。
- 标签类别经作者测试标签与分类 XML 对照核验：0=mandatory（指示标志），1=prohibitory（禁令标志），2=warning（警告标志）。
- 作者只提供训练和测试划分，没有独立验证集。训练时应从训练集另划验证集，测试集留作最终评估。
- 原始 ZIP 保留以便核对；解压后的 train/images、train/labels、test/images、test/labels 用于实验。
- 本地核验：训练与测试图像、TXT 标注均一一对应；标签框字段有效且归一化坐标位于 0 到 1。测试集 3228 个框中，指示 718、禁令 2177、警告 333，与数据论文公布的统计一致。
