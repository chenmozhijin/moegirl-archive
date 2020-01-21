# 萌娘百科存档工具

![python 3.8](https://img.shields.io/badge/python-3.8-blue.svg?logo=python)
![test: passed](https://img.shields.io/badge/test-passed-brightgreen.svg)
[![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/mit-license.php)

葫芦又写于2020年1月21日。

**存档[萌娘百科](https://zh.moegirl.org/)中文站的指定页面的维基文本。**

萌娘百科®、Moegirlpedia®是注册商标。此程序仅提供存档功能。有关使用存档的内容时需遵守的版权协定，请参阅[萌娘百科的版权信息](https://zh.moegirl.org/萌娘百科:版权信息)。

## 注意

此程序“**按原样**”提供。请在运行之前按你的需要调整其中的内容。本人不负责提供教程等。

本程序依赖萌娘百科的API。有关API的内容，参见[萌娘百科的API沙盒](https://zh.moegirl.org/Special:ApiSandbox)。

在安装完成Python之后，需要额外安装`requests`包。或者请自行修改代码为使用`urllib`等。

## 使用方法

1. 在`PAGELIST.txt`中按格式写入你存档的页面的类型、ID、标题。中间用制表符`	`隔开。  
页面类型可以随意定义。可以根据需要对页面进行分类，然后只存档需要的类型的页面。  
如果不知道其中的某个值，可以空出。但需要保证所有页面的都给出了某一值，比如都给出了页面ID。

2. 在同目录下创建文件夹`archive/`。在文件夹中创建文本文档`!.txt`。文本文档的初始内容为`{}`。  
注意：初次存档时，文本文档的初始内容一定要手动设置好。  
存档将存放在文件夹中，文本文档将记录存档的数据，以便下次存档时读取。

3. 运行`moegirl_archive.py`，按下`Enter`键开始存档。  
屏幕上将显示存档的过程。网络出现问题时，会输出一个`.`并自动重试。  
`[存][新]`表示这是第一次存档这个页面。  
`[存][覆盖]`表示之前存档过这个页面，本次存档覆盖了之前的存档。  
`[提示][移]`表示之前的存档中的页面标题与实际页面标题不一致，即在上次存档之后页面被移动至新的标题。  
`-`在上次存档后没有发生变化后的页面，本次存档时会跳过。将第87行的`#`删掉即可在屏幕上输出被跳过的页面的信息。

初次存档，存档1000个页面大约需要20分钟。覆盖原有存档，则要看有多少页面需要覆盖。

## 你可能需要修改的代码

* 第16～18行，页面列表、存档存放的文件夹、记录存档的数据文件。
* 第25、37行，文件的编码。
* 第30行，需要存档的页面的类型代码。
* 第82行，在页面标题中遇到不能作为文件名的字符时的转换列表。
* 第126～128行，放在存档数据中的备注信息，包括备注文字、时间、计算机名。您可以手动修改为自定义的文字。
* 本程序中是按照页面ID查找页面的。如果需要改成根据页面标题查找，需要改动的地方有：第28～31、52～55、65、69、78~81、83～84、86~87、93～94、100~101、108～109、112、119～124行。自己改哈。

## 注释

`PID` = `Page ID`，页面编号

`RID` = `Revision ID`，历史版本编号

存放数据的文件中按照``{pageid: [revid, title], ...}``的格式存储。

示例文件中的`PAGELIST.txt`和`!.txt`是已经运行过一次的结果，但示例文件中没有给出存档结果。

请注意，在存档之后如果人为将存档文件移动或删除，或对数据进行修改，再次存档时将无法识别这些变化，可能不能按预期存档；特别是当文件被修改，但数据没有变动，同时页面也没有被编辑时，可能不会用新内容覆盖旧内容。  

初次存档请按照[上文](#使用方法)设置数据文件的初始内容。

~~示例文件的页面列表其实是萌娘百科LoveLive!系列的全部页面。~~

## 已知问题

1. 不会识别标题被替换的页面的标题，包括首字母小写标题。存档中将全部按照页面的真实标题记录。
2. 因为要不断和服务器提交请求并获取数据，所以运行有点慢。这不是问题。
3. 存档是维基文本的格式。没有指定需要存档的文件、模板等不会被存档。这也意味着直接将存档的内容复制到其他维基网站可能无法按预期显示。
4. 不能存档文件。一是因为维基的文件不是以维基文本的格式存储的，二是因为萌娘百科的大多数文件都是放在[萌娘共享](https://commons.moegirl.org/)上的。
5. 我觉得我做得挺完美的。如果还有问题，请在[Issues](https://github.com/huxiangyou/moegirl-archive/issues)提出。