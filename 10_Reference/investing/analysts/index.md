# 分析师 索引

> 研报作者节点。对应 Pydantic 契约 `Report.researcher`。每位分析师链接其覆盖领域、近期研报、历史评级胜率。

## 实体列表（Dataview 动态）

```dataview
TABLE name AS "姓名", org AS "机构", coverage_count AS "覆盖数"
FROM "analysts"
WHERE type = "analyst"
SORT name ASC
```

## 关系

- authored: [[reports/]]（该分析师的研报）
- covers: [[stocks/]]（该分析师覆盖的个股，通过研报间接关联）
- sourced_from: [[data-sources/]]（分析师排名数据来源）

## 新建实体

用 Templater 应用 `templates/analyst` 新建。

## 实体清单（入边）

> 本段手工列出实体以建立入边链接（Dataview 表格不计入边）。

- [[analysts/Austin Liang-招银国际]] — Austin Liang @ 招银国际
- [[analysts/Ji SHI-招银国际]] — Ji SHI @ 招银国际
- [[analysts/Wenjing Dou-招银国际]] — Wenjing Dou @ 招银国际
- [[analysts/于芳-华鑫证券]] — 于芳 @ 华鑫证券
- [[analysts/何鹏程-华鑫证券]] — 何鹏程 @ 华鑫证券
- [[analysts/倪爽-华金证券]] — 倪爽 @ 华金证券
- [[analysts/刘天文-开源证券]] — 刘天文 @ 开源证券
- [[analysts/刘孟峦-国信证券]] — 刘孟峦 @ 国信证券
- [[analysts/刘强-太平洋]] — 刘强 @ 太平洋
- [[analysts/刘虹辰-太平洋]] — 刘虹辰 @ 太平洋
- [[analysts/叶子-国信证券]] — 叶子 @ 国信证券
- [[analysts/叶泽佑-西南证券]] — 叶泽佑 @ 西南证券
- [[analysts/吴文吉-中邮证券]] — 吴文吉 @ 中邮证券
- [[analysts/周尔双-东吴证券]] — 周尔双 @ 东吴证券
- [[analysts/周涛-华金证券]] — 周涛 @ 华金证券
- [[analysts/周源-东吴证券]] — 周源 @ 东吴证券
- [[analysts/周莎-太平洋]] — 周莎 @ 太平洋
- [[analysts/和芳芳-山西证券]] — 和芳芳 @ 山西证券
- [[analysts/孙山山-华鑫证券]] — 孙山山 @ 华鑫证券
- [[analysts/孙远峰-华金证券]] — 孙远峰 @ 华金证券
- [[analysts/宇之光-国元证券]] — 宇之光 @ 国元证券
- [[analysts/宋辰超-太平洋]] — 宋辰超 @ 太平洋
- [[analysts/宋鹏-华金证券]] — 宋鹏 @ 华金证券
- [[analysts/庄宇-华鑫证券]] — 庄宇 @ 华鑫证券
- [[analysts/张大为-国信证券]] — 张大为 @ 国信证券
- [[analysts/张天-山西证券]] — 张天 @ 山西证券
- [[analysts/张子健-中邮证券]] — 张子健 @ 中邮证券
- [[analysts/张璐-华鑫证券]] — 张璐 @ 华鑫证券
- [[analysts/张衡-国信证券]] — 张衡 @ 国信证券
- [[analysts/徐剑峰-开源证券]] — 徐剑峰 @ 开源证券
- [[analysts/徐怡然-山西证券]] — 徐怡然 @ 山西证券
- [[analysts/戴筝筝-华金证券]] — 戴筝筝 @ 华金证券
- [[analysts/方闻千-华金证券]] — 方闻千 @ 华金证券
- [[analysts/景丹阳-华龙证券]] — 景丹阳 @ 华龙证券
- [[analysts/曹佩-太平洋]] — 曹佩 @ 太平洋
- [[analysts/曾朵红-东吴证券]] — 曾朵红 @ 东吴证券
- [[analysts/朱会振-西南证券]] — 朱会振 @ 西南证券
- [[analysts/朱吉翔-群益证券]] — 朱吉翔 @ 群益证券
- [[analysts/朱正卿-民生证券]] — 朱正卿 @ 民生证券
- [[analysts/朱珠-华鑫证券]] — 朱珠 @ 华鑫证券
- [[analysts/李书颖-国信证券]] — 李书颖 @ 国信证券
- [[analysts/李全-国信证券]] — 李全 @ 国信证券
- [[analysts/李宏涛-华金证券]] — 李宏涛 @ 华金证券
- [[analysts/李帅华-中邮证券]] — 李帅华 @ 中邮证券
- [[analysts/李林卉-太平洋]] — 李林卉 @ 太平洋
- [[analysts/李柳晓-交银国际证券]] — 李柳晓 @ 交银国际证券
- [[analysts/李美贤-华安证券]] — 李美贤 @ 华安证券
- [[analysts/李育文-中银证券]] — 李育文 @ 中银证券
- [[analysts/李蕙-华金证券]] — 李蕙 @ 华金证券
- [[analysts/杜羽枢-山西证券]] — 杜羽枢 @ 山西证券
- [[analysts/杜致远-开源证券]] — 杜致远 @ 开源证券
- [[analysts/杨丰源-中邮证券]] — 杨丰源 @ 中邮证券
- [[analysts/杨帅波-中邮证券]] — 杨帅波 @ 中邮证券
- [[analysts/杨耀洪-国信证券]] — 杨耀洪 @ 国信证券
- [[analysts/梁必果-太平洋]] — 梁必果 @ 太平洋
- [[analysts/沈嘉婕-群益证券]] — 沈嘉婕 @ 群益证券
- [[analysts/熊军-华金证券]] — 熊军 @ 华金证券
- [[analysts/熊鹏-山西证券]] — 熊鹏 @ 山西证券
- [[analysts/王兴网-西南证券]] — 王兴网 @ 西南证券
- [[analysts/王思-中邮证券]] — 王思 @ 中邮证券
- [[analysts/王晓萱-中邮证券]] — 王晓萱 @ 中邮证券
- [[analysts/王海维-华金证券]] — 王海维 @ 华金证券
- [[analysts/王蔚祺-国信证券]] — 王蔚祺 @ 国信证券
- [[analysts/石俊烨-华鑫证券]] — 石俊烨 @ 华鑫证券
- [[analysts/祁海超-开源证券]] — 祁海超 @ 开源证券
- [[analysts/程漫漫-太平洋]] — 程漫漫 @ 太平洋
- [[analysts/罗通-开源证券]] — 罗通 @ 开源证券
- [[analysts/翟一梦-中邮证券]] — 翟一梦 @ 中邮证券
- [[analysts/肖索-山西证券]] — 肖索 @ 山西证券
- [[analysts/胡慧-国信证券]] — 胡慧 @ 国信证券
- [[analysts/舒尚立-西南证券]] — 舒尚立 @ 西南证券
- [[analysts/苏铖-东吴证券]] — 苏铖 @ 东吴证券
- [[analysts/蒋颖-开源证券]] — 蒋颖 @ 开源证券
- [[analysts/蔡雪昱-中邮证券]] — 蔡雪昱 @ 中邮证券
- [[analysts/袁文翀-国信证券]] — 袁文翀 @ 国信证券
- [[analysts/裴伊凡-中航证券]] — 裴伊凡 @ 中航证券
- [[analysts/詹浏洋-国信证券]] — 詹浏洋 @ 国信证券
- [[analysts/贺朝晖-华金证券]] — 贺朝晖 @ 华金证券
- [[analysts/赵悦媛-开源证券]] — 赵悦媛 @ 开源证券
- [[analysts/连欣然-国信证券]] — 连欣然 @ 国信证券
- [[analysts/邓健全-开源证券]] — 邓健全 @ 开源证券
- [[analysts/邓天娇-中银证券]] — 邓天娇 @ 中银证券
- [[analysts/郑磊-太平洋]] — 郑磊 @ 太平洋
- [[analysts/郝润祺-国元证券]] — 郝润祺 @ 国元证券
- [[analysts/郭念伟-中航证券]] — 郭念伟 @ 中航证券
- [[analysts/阮巧燕-东吴证券]] — 阮巧燕 @ 东吴证券
- [[analysts/陈天瑜-中邮证券]] — 陈天瑜 @ 中邮证券
- [[analysts/陈庆-交银国际证券]] — 陈庆 @ 交银国际证券
- [[analysts/陈瑶蓉-国信证券]] — 陈瑶蓉 @ 国信证券
- [[analysts/陈耀波-华安证券]] — 陈耀波 @ 华安证券
- [[analysts/陈蓉芳-开源证券]] — 陈蓉芳 @ 开源证券
- [[analysts/陈雯-万联证券]] — 陈雯 @ 万联证券
- [[analysts/陶泽-东吴证券]] — 陶泽 @ 东吴证券
- [[analysts/韩晨-西南证券]] — 韩晨 @ 西南证券
- [[analysts/顾向君-群益证券]] — 顾向君 @ 群益证券
- [[analysts/马佳伟-民生证券]] — 马佳伟 @ 民生证券
- [[analysts/马天诣-民生证券]] — 马天诣 @ 民生证券
- [[analysts/黄细里-东吴证券]] — 黄细里 @ 东吴证券
- [[analysts/黄铮-国信证券]] — 黄铮 @ 国信证券
