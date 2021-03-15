# Do Thinking

* MarkDown语法编辑文章，兼顾美观性和便捷性
* 依赖MathJex实现Latex语法编辑公式
* 本地的及时备份

## 语法参考

### 文件头
```python
---
layout      : post                         # 使用post模板
title       : hello world                  # 文章标题
description : Markdown Cheatsheet Demo...  # 文章概要
keywords    : markdown, 语法, Latex         # 关键字
tags        : [markdown, readme]           # 文章标签
mathjax     : true                         # 是否使用Latex，需要的话则引入mathjex引擎
---
```

<div class="divider"></div>

### 六级标题：H1-H6

# H1 Heading

## H2 Heading

### H3 Heading

#### H4 Heading

##### H5 Heading

###### H6 Heading

<div class="divider"></div>

### 文本样式 

可以使用`**sth**`来**加粗文本**，使用`_sth_`来_获得斜体效果_；当然，**_二者可以组合使用_**。`sth`可以`高亮文本`。

超链接形式为：`[文本](地址)` ，例如[http://www.example.com](http://www.example.com)。

`>`引导引用文本：
> 这是一段引用文字。

<div class="divider"></div>

### 脚注

使用`[[^1]]`可以添加脚注 [[^1]]，依次继续添加 [[^2]]。

<div class="divider"></div>

## 列表项

1. 有序列表项1
2. 有序列表项2

* `*`引导无序列表
- `-`也可以引导无序列表
+ `+`同样引导无序列表

<div class="divider"></div>

### 代码块

```javascript
var s = "JavaScript syntax highlighting";
alert(s);
```

```python
s = "Python syntax highlighting"
print s
```

```
No language indicated, so no syntax highlighting.
But let's throw in a <b>tag</b>.
```

<div class="divider"></div>

### 表格

#### 使用`:`表示对齐方式

| Tables        | Are           | Cool  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | $1600 |
| col 2 is      | centered      | $12   |
| zebra stripes | are neat      | $1    |

#### 自由边线表格

Markdown | Less | Pretty
--- | --- | ---
*Still* | `renders` | **nicely**
1 | 2 | 3

<div class="divider"></div>

### 水平线

The HTML `<hr>` element is for creating a "thematic break" between paragraph-level elements. In markdown, you can create a `<hr>` with any of the following:

* `___`: three consecutive underscores
* `---`: three consecutive dashes
* `***`: three consecutive asterisks

效果分别为:

___

---

***

<div class="divider"></div>

### 图片

根据本项目中图片文件夹的路径，采用`![图片注释]({{ "/images/test.png" | prepend: site.baseurl }})`显示图片。

或者也可以使用`<img>`标签插入图片：

1. `<img src="{{ "/images/test.png" | prepend: site.baseurl }}">`
2. `<div align='center'><img src="{{ "/images/test.png" | prepend: site.baseurl }}" width="200"></div>`

<div class="divider"></div>

### MathJax编写Latex公式

1. `$sth$`表示行内公式，`$$sth$$`或者`\\[sth\\]`表示行间公式，此时对于界定符号之内的latex代码无需进行转义
2. 多行对齐公式（无编号）使用`\begin{align\*}`和`\end{align\*}`，注意此时**需要对latex代码进行必要的转义**：

* `*`需要转义`\*`
* 下标`_`需要转义为`\_`
* 换行符`\\`需要转义为`\\\\\\`

公式编号可以使用`\begin{equation}`或者`\begin{align}`环境

---
脚注内容:

[^1]: 1: 这是脚注1.

[^2]: 2: 脚注也可以是超链接 - [click here!](#)

## LICENSE

* `_posts`中文章及`images`中相应图片采用[署名-非商业性使用-相同方式共享](http://creativecommons.org/licenses/by-nc-sa/3.0/)协议进行授权，转载请注明来源

* 站点其他代码采用[MIT License 许可](http://zh.wikipedia.org/wiki/MIT_License)

## 致谢

基于[**Heiswayi Nrird**](http://heiswayi.github.io/)贡献的Jekyll主题[**Thinkspace**](https://github.com/heiswayi/thinkspace)修改。

