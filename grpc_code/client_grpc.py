import grpc
from . import ee613_team_pb2 as pb
from . import ee613_team_pb2_grpc as pb_grpc
import data_class as dc

# Food Order Class
class Food_Order_C():
    def __init__(self):
        self.Total_Cost = 0
        self.order_dict = {}
    
    def add_order(self, menu_id, menu_num, menu_cost):
        self.order_dict[menu_id] = menu_num
        self.Total_Cost += menu_cost

# Login / Refreshing the menu info
def grpc_Login(stub, usrid, usrpwd):
    Request = pb.User_Info(u_id=usrid, u_pwd=usrpwd)
    Response = stub.Login_(Request)
    # save the food info
    for menus in Response.fd_info:
        dc.menu_info[menus.menu_id] = [menus.menu_name, menus.menu_price, menus.menu_num]
    # print(dc.menu_info)
    return Response.login_success

# Sigin
def grpc_Signup(stub, usrid, usrpwd):
    Request = pb.User_Info(u_id=usrid, u_pwd=usrpwd)
    Response = stub.Signin(Request)
    if (Response.signin_success):
        return True
    else:
        return False

# Order_Food
def grpc_OrderFood(stub, orders_info, total_cost):
    Request_uif = pb.User_Info(u_id=dc.login_info['id'], u_pwd=dc.login_info['pwd'])
    orders = []
    for menu_id in orders_info:
        orders.append(pb.Orders_(menu_id=menu_id, menu_num=orders_info[menu_id]))
    Request = pb.Food_Order(orders_=orders, total_cost=total_cost, uif=Request_uif)
    Response = stub.Order_Food(Request)
    return Response.istrue, Response.remaining_points

# Point Check
def grpc_CheckPoint(stub, usrid, usrpwd):
    Request = pb.User_Info(u_id=usrid, u_pwd=usrpwd)
    Response = stub.Point_Check(Request)
    return Response.remaining_points

# Point Recharge
def grpc_RechargePoint(stub, usrid, usrpwd, rpoints):
    Request_uif = pb.User_Info(u_id=usrid, u_pwd=usrpwd)
    Request = pb.Recharge_Request(uif=Request_uif, recharging_points=rpoints)
    Response = stub.Point_Recharge(Request)
    return Response.remaining_points

# gRPC Initialize
def grpc_Initialize():
    channel = grpc.insecure_channel('localhost:9999')
    stub = pb_grpc.EE613_Team_PStub(channel)
    return stub
