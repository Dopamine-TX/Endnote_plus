#### endnote内置的自定义函数问题

##### 尝试1

* 通过python接口`create_collation`定义同名排序规则  （目前endnote_plus.py中已经有了）

* 通过python接口**`create_function`**定义同名自定义函数 （https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.create_function）

* 但运行后报错

  ```bash
  sqlite3.DatabaseError: database disk image is malformed
  ```

  可能是自己定义的同名函数功能上与内置的不同 导致了数据库损坏？

##### 尝试2

* 这些内置函数定义在何处？
  * 在3个数据库中查找，没有发现定义
  * 应该是定义在endnote程序包中 能否通过逆向工具查看并提取？
  * 使用Dependency Walker 查看程序安装目录中的libmysqld.dll中的接口，未发现相关定义
  * 可能是在endnote.exe主程序中。逆向工具不太会用，先放弃。

##### 尝试3

* 将原数据库导出成sql语句，并暂存到`tmp.sql`中：

  ```bash
  $ sqlite3 sdb.db
  sqlite> .output tmp.sql
  sqlite> .dump
  ```

* 查看`tmp.sql`后发现，含有内置自定义函数的语句主要包括：

  ```sqlite
  CREATE TABLE terms( list_id INTEGER UNSIGNED NOT NULL,  term TEXT NOT NULL COLLATE ENCI_Base);
  
  CREATE TABLE jterms( list_id INTEGER UNSIGNED NOT NULL,  packed_term TEXT NOT NULL COLLATE ENCI_Base,  term  TEXT NOT NULL COLLATE ENCI_Base,  abbr1 TEXT NOT NULL COLLATE ENCI_Base DEFAULT "",  abbr2 TEXT NOT NULL COLLATE ENCI_Base DEFAULT "",  abbr3 TEXT NOT NULL COLLATE ENCI_Base DEFAULT "");
  
  CREATE TRIGGER refs__refs_ord_AI  AFTER INSERT ON refs BEGIN INSERT INTO refs_ord (ro_trash_state, ro_key_2, ro_key_3, ro_id) VALUES (new.trash_state, EN_MAKE_SORT_KEY(new.author,2,12), EN_MAKE_SORT_KEY(new.year,3,12), new.id); END;
  
  CREATE TRIGGER refs__refs_ord_AU  AFTER UPDATE ON refs BEGIN DELETE FROM refs_ord WHERE ro_id = old. id;INSERT INTO refs_ord (ro_trash_state, ro_key_2, ro_key_3, ro_id) VALUES (new.trash_state, EN_MAKE_SORT_KEY(new.author,2,12), EN_MAKE_SORT_KEY(new.year,3,12), new.id); END;
  
  ```

* 对上面这些语句作编辑：

  * 删除前两句中的`COLLATE ENCI_Base` （副作用？）
  * 删除含有`EN_MAKE_SORT_KEY`的后两个语句 （副作用：会导致refs_ord表的内容不能正确更新）

* 将编辑后的语句导入新库sdb2.db

  ```sqlite
  $ sqlite3 sdb2.db
  sqlite> .read tmp.sql
  ```

* sdb2.db的内容和原库基本一致 但不包含endnote内置的自定义函数 所以可以运行`endnote_plus.py`正常update

* 后续问题：

  * 修改后（去掉排序规则、去掉两个TRIGGER）后的数据库，是否能被endnote正常读取和使用？
  * 修改后的数据库被endnote打开后 是否会被修正成正常状态？（加回排序规则和trigger?) 可以测试并确认。
  * 含有内置自定义函数的语句的具体含义？能否猜测出相关内置函数的功能？