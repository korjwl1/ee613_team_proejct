import grpc
from . import ee613_team_pb2 as pb
from . import ee613_team_pb2_grpc as pb_grpc

# Food Order Class
class Food_Order_C():
    def __init__(self):
        self.Total_Cost = 0
        self.order_dict = {}
    
    def add_order(self, menu_id, menu_num, menu_cost):
        self.order_dict[menu_id] = menu_num
        self.Total_Cost += menu_cost

# Login 
def grpc_Login(stub, usrid, usrpwd):
    Request = pb.User_Info(u_id=usrid, u_pwd=usrpwd)
    Response = stub.Login_(Request)
    return Response.login_success, Response.fd_info

# Sigin
def grpc_Signup(stub, usrid, usrpwd):
    Request = pb.User_Info(u_id=usrid, u_pwd=usrpwd)
    Response = stub.Signin(Request)
    if (Response.signin_success):
        return True
    else:
        return False

# Order_Food
def grpc_OrderFood(stub, usrid, usrpwd, orderinfo):
    Request_uif = pb.User_Info(u_id=usrid, u_pwd=usrpwd)
    return None

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
