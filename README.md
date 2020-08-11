# Spider Plant Cell

## 使用

首先注册百度翻译帐号，获取API相关信息，然后修改``脚本的第44和45行👇
```
appid = ''
secretKey = ''
```
修改第227行可选取爬取的起始和终止年限👇
```
film = parse_detail_page(1989, 2021, tool)
```
之后运行`python Spider_Plant_Cell.py` 即可开始爬取。
## 结果输出
### CSV 文件
```
2004	A CDC45 Homolog in Arabidopsis Is Essential for Meiosis, as Shown by RNA Interference–Induced Gene Silencing	如RNA干扰诱导的基因沉默所示，拟南芥CDC45同系物对减数分裂至关重要	http://www.plantcell.org/content/16/1/99
2007	A CLASSY RNA Silencing Signaling Mutant in Arabidopsis	拟南芥一个RNA沉默信号突变株	http://www.plantcell.org/content/19/5/1439
2007	A CRM Domain Protein Functions Dually in Group I and Group II Intron Splicing in Land Plant Chloroplasts	陆地植物叶绿体中CRM结构域蛋白在Ⅰ组和Ⅱ组内含子剪接中的双重功能	http://www.plantcell.org/content/19/12/3864
2015	A Cascade of Sequentially Expressed Sucrose Transporters in the Seed Coat and Endosperm Provides Nutrition for the Arabidopsis Embryo	种皮和胚乳中蔗糖转运蛋白的级联表达为拟南芥胚胎提供了营养	http://www.plantcell.org/content/27/3/607
2011	A Case for Spatial Regulation in Tetrapyrrole Biosynthesis	四吡咯生物合成的空间调控	http://www.plantcell.org/content/23/12/4167
2001	A Cell Plate–Specific Callose Synthase and Its Interaction with Phragmoplastin	细胞板特异性胼胝质合成酶及其与胞浆蛋白的相互作用	http://www.plantcell.org/content/13/4/755
2009	A Cell Wall–Degrading Esterase of Xanthomonas oryzae Requires a Unique Substrate Recognition Module for Pathogenesis on Rice	水稻黄单胞菌的细胞壁降解酯酶需要一个独特的底物识别模块来研究水稻的发病机制	http://www.plantcell.org/content/21/6/1860
```
### 标题词云
![](baidu_Plant_Cell_Articles.png)
