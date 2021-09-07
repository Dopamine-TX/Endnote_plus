## endnote数据条目批量编辑工具

### 需求描述

* 根据实际使用需要，对endnote数据库中的条目作批量自动化编辑，完成官方软件中未提供或不能批量处理的功能。
* 功能点举例
  * 标题文本的大小写切换（句首大写/每单词首字母大写/全小写等)
  * 杂志名及缩写标准化
  * ……

### 实现方案

#### 尝试方案一  （不好，可不考虑，仅作记录)

* 尝试导出为xml  编辑后再导入
  * 可以正常导出导入
  * 有相关库可以读取和修改xml文件
  * 但部分信息在导出时丢失，比如导出时无法导出文献目录信息 

#### 尝试方案二 (可能可行，可尝试)

* 观察与测试后发现，endnote数据库实际上都是sqlite3数据库

* 直接使用相关工具(比如python sqlite3库 https://docs.python.org/3/library/sqlite3.html)对sqlite3数据库中的条目进行读取与编辑，保存为新数据库

* TODO:

  * 需要弄清每张表与主要条目的含义
  * 不同表的数据可能有关联。在修改时如何保证数据的一致性，并保证官方软件可以正常读取
  
* 数据库表项整理(基于X9.3.1版本)

  * 主数据库 （保存时命名的数据库)

    * enl_refs

    * ```sqlite
      0|id|INTEGER|0||1
      1|trash_state|INTEGER|1|0|0
      2|text_styles|TEXT|1|""|0
      3|reference_type|INTEGER|1|0|0
      4|author|TEXT|1|""|0
      5|year|TEXT|1|""|0
      6|title|TEXT|1|""|0
      7|pages|TEXT|1|""|0
      8|secondary_title|TEXT|1|""|0
      9|volume|TEXT|1|""|0
      10|number|TEXT|1|""|0
      11|number_of_volumes|TEXT|1|""|0
      12|secondary_author|TEXT|1|""|0
      13|place_published|TEXT|1|""|0
      14|publisher|TEXT|1|""|0
      15|subsidiary_author|TEXT|1|""|0
      16|edition|TEXT|1|""|0
      17|keywords|TEXT|1|""|0
      18|type_of_work|TEXT|1|""|0
      19|date|TEXT|1|""|0
      20|abstract|TEXT|1|""|0
      21|label|TEXT|1|""|0
      22|url|TEXT|1|""|0
      23|tertiary_title|TEXT|1|""|0
      24|tertiary_author|TEXT|1|""|0
      25|notes|TEXT|1|""|0
      26|isbn|TEXT|1|""|0
      27|custom_1|TEXT|1|""|0
      28|custom_2|TEXT|1|""|0
      29|custom_3|TEXT|1|""|0
      30|custom_4|TEXT|1|""|0
      31|alternate_title|TEXT|1|""|0
      32|accession_number|TEXT|1|""|0
      33|call_number|TEXT|1|""|0
      34|short_title|TEXT|1|""|0
      35|custom_5|TEXT|1|""|0
      36|custom_6|TEXT|1|""|0
      37|section|TEXT|1|""|0
      38|original_publication|TEXT|1|""|0
      39|reprint_edition|TEXT|1|""|0
      40|reviewed_item|TEXT|1|""|0
      41|author_address|TEXT|1|""|0
      42|caption|TEXT|1|""|0
      43|custom_7|TEXT|1|""|0
      44|electronic_resource_number|TEXT|1|""|0
      45|translated_author|TEXT|1|""|0
      46|translated_title|TEXT|1|""|0
      47|name_of_database|TEXT|1|""|0
      48|database_provider|TEXT|1|""|0
      49|research_notes|TEXT|1|""|0
      50|language|TEXT|1|""|0
      51|access_date|TEXT|1|""|0
      52|last_modified_date|TEXT|1|""|0
      53|record_properties|TEXT|1|""|0
      54|added_to_library|INTEGER|1|0|0
      55|record_last_updated|INTEGER|1|0|0
      56|reserved3|INTEGER|1|0|0
      57|fulltext_downloads|TEXT|1|""|0
      58|read_status|TEXT|1|""|0
      59|rating|TEXT|1|""|0
      60|reserved7|TEXT|1|""|0
      61|reserved8|TEXT|1|""|0
      62|reserved9|TEXT|1|""|0
      63|reserved10|TEXT|1|""|0
      ```

  * sdb.eni: csort     file_res  groups    jterms    misc      refs      refs_ord  terms

  * sdb.eni

    * csort

      ```sqlite
      0|id|INTEGER|0||1
      1|mru_rank|INTEGER|1|0|0
      2|sort_type|INTEGER|1||0
      3|sort_spec|TEXT|1||0
      4|sorted_order|BLOB|1||0
      ```

    * file_res

      ```sqlite
      0|refs_id|INTEGER|1||0
      1|file_path|TEXT|1|""|0
      2|file_type|INTEGER|1||0
      3|file_pos|INTEGER|1||0
      ```

    * groups

      ```sqlite
      0|group_id|INTEGER|0||1
      1|recs_stamp|INTEGER UNSIGNED|1|0|0
      2|spec|BLOB|1|""|0
      3|members|BLOB|1|""|0
      ```

    * jterms

      ```sqlite
      0|list_id|INTEGER UNSIGNED|1||0
      1|packed_term|TEXT|1||0
      2|term|TEXT|1||0
      3|abbr1|TEXT|1|""|0
      4|abbr2|TEXT|1|""|0
      5|abbr3|TEXT|1|""|0
      ```

      

    * misc

      ```sqlite
      0|code|INTEGER UNSIGNED|1||1
      1|subcode|INTEGER UNSIGNED|1||2
      2|value|BLOB|1||0
      ```

    * refs

      ```sqlite
      0|code|INTEGER UNSIGNED|1||1
      1|subcode|INTEGER UNSIGNED|1||2
      2|value|BLOB|1||0
      sqlite> PRAGMA table_info(refs);
      0|id|INTEGER|0||1
      1|trash_state|INTEGER|1|0|0
      2|text_styles|TEXT|1|""|0
      3|reference_type|INTEGER|1|0|0
      4|author|TEXT|1|""|0
      5|year|TEXT|1|""|0
      6|title|TEXT|1|""|0
      7|pages|TEXT|1|""|0
      8|secondary_title|TEXT|1|""|0
      9|volume|TEXT|1|""|0
      10|number|TEXT|1|""|0
      11|number_of_volumes|TEXT|1|""|0
      12|secondary_author|TEXT|1|""|0
      13|place_published|TEXT|1|""|0
      14|publisher|TEXT|1|""|0
      15|subsidiary_author|TEXT|1|""|0
      16|edition|TEXT|1|""|0
      17|keywords|TEXT|1|""|0
      18|type_of_work|TEXT|1|""|0
      19|date|TEXT|1|""|0
      20|abstract|TEXT|1|""|0
      21|label|TEXT|1|""|0
      22|url|TEXT|1|""|0
      23|tertiary_title|TEXT|1|""|0
      24|tertiary_author|TEXT|1|""|0
      25|notes|TEXT|1|""|0
      26|isbn|TEXT|1|""|0
      27|custom_1|TEXT|1|""|0
      28|custom_2|TEXT|1|""|0
      29|custom_3|TEXT|1|""|0
      30|custom_4|TEXT|1|""|0
      31|alternate_title|TEXT|1|""|0
      32|accession_number|TEXT|1|""|0
      33|call_number|TEXT|1|""|0
      34|short_title|TEXT|1|""|0
      35|custom_5|TEXT|1|""|0
      36|custom_6|TEXT|1|""|0
      37|section|TEXT|1|""|0
      38|original_publication|TEXT|1|""|0
      39|reprint_edition|TEXT|1|""|0
      40|reviewed_item|TEXT|1|""|0
      41|author_address|TEXT|1|""|0
      42|caption|TEXT|1|""|0
      43|custom_7|TEXT|1|""|0
      44|electronic_resource_number|TEXT|1|""|0
      45|translated_author|TEXT|1|""|0
      46|translated_title|TEXT|1|""|0
      47|name_of_database|TEXT|1|""|0
      48|database_provider|TEXT|1|""|0
      49|research_notes|TEXT|1|""|0
      50|language|TEXT|1|""|0
      51|access_date|TEXT|1|""|0
      52|last_modified_date|TEXT|1|""|0
      53|record_properties|TEXT|1|""|0
      54|added_to_library|INTEGER|1|0|0
      55|record_last_updated|INTEGER|1|0|0
      56|reserved3|INTEGER|1|0|0
      57|fulltext_downloads|TEXT|1|""|0
      58|read_status|TEXT|1|""|0
      59|rating|TEXT|1|""|0
      60|reserved7|TEXT|1|""|0
      61|reserved8|TEXT|1|""|0
      62|reserved9|TEXT|1|""|0
      63|reserved10|TEXT|1|""|0
      ```

    * refs_ord

      ```sqlite
      0|ro_trash_state|INTEGER|0||0
      1|ro_key_2|TEXT|0||0
      2|ro_key_3|TEXT|0||0
      3|ro_id|INTEGER|0||1
      ```

    * terms

      ```sqlite
      0|list_id|INTEGER UNSIGNED|1||0
      1|term|TEXT|1||0
      ```

  * pdb.eni

    * pdf_index

      ```sqlite
      0|pdfi_id|INTEGER|0||1
      1|version|INTEGER UNSIGNED|1|0|0
      2|refs_id|INTEGER UNSIGNED|1|0|0
      3|file_timestamp|INTEGER UNSIGNED|1|0|0
      4|subkey|BLOB|1||0
      5|contents|TEXT|1|""|0
      6|tag|TEXT|1|""|0
      ```

      

