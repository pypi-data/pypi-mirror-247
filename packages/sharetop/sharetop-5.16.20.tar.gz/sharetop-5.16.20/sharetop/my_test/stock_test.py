import sharetop as sp

token = "72d17b9a46de80bf"
sp_obj = sp.sp_prepare.BasicTop(token)

# r = sp_obj.common_exec_func("stock_to_stock_bonus", {"limit": 10, "is_explain": True, "ts_code": "002049.SZ"})
#
# print(r.to_dict("records"))


r2 = sp_obj.common_exec_func("stock_to_stock_repurchase", {"limit": 10, "is_explain": False, "start_notice_date": "2023-12-12"})

print(r2.to_dict("records"))