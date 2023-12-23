<h1>1、模块介绍</h1>
<p>本模块是为了实现CST数据格式转化为DATE类型而写的。</p>
<p>转换示例：</p>
<p>Tue Nov 14 09:35:17 CST 2023 <p>转化为</p> 2023-12-14 09:35:17</p>
<p>代码调用示例：</p>
<p>
import csttodate<br>
#读取path路径的excel，并完成col列数据转换。excel仅支持xlsx格式，需要使用openpyxl模块。
<br>read_excel(path,col,save_path)<br>
res=cst_to_date(cstdate)<br>

</p>