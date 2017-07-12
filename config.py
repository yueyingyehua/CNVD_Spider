# coding:UTF8

class Config():
    vul_list = {
        "chname":'chname',
        "CNVD-ID": "cnvd_id",
        "发布时间": "release_time",
        "危害级别": "vul_level",
        "影响产品 ": "impact_product",
        "BUGTRAQ ID": "bugtraq_id",
        "CVE ID": "cve_id",
        "漏洞描述": "vul_description",
        "漏洞类型": "vul_type",
        "参考链接": "reference_link",
        "漏洞解决方案": "vul_solution",
        "漏洞发现者": "finder",
        "厂商补丁": "vendor_patch",
        "验证信息": "validation_info",
        "报送时间": "submission_time",
        "收录时间": "included_time",
        "更新时间": "update_time",
        "漏洞附件": "vul_attachment",
    }

    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36"
    accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    accept_Encoding = "gzip, deflate, sdch"
    accept_Language = "zh-CN,zh;q=0.8"
    header = {"User-Agent" : user_agent,"Accept-Language" : accept_Language,
              "Accept_Encoding" : accept_Encoding, "Accept" : accept}

