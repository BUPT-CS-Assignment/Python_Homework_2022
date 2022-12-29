from core.crawler import catch
from core.geo import crawl_position_citys
from process import *
from analyze import *

if __name__ == '__main__':
    init_db()                           # 数据库初始化
    catch(recap_cbd=True)               # 数据抓取
    check_db()                          # 初步数据统计
    crawl_position_citys()              # CBD经纬度获取
    export_csv()                        # csv导出
    extract()                           # 数据处理整合
    plot_price_types(origin=False)      # 原始分布情况绘制
    exception_process()                 # 异常数据处理
    plot()                              # 最终数据绘制
    
    








